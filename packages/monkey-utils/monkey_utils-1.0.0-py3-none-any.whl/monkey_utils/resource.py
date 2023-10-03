import os 
import boto3  
import asyncio
import zipfile
import argparse
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

class S3Connection:

    def __init__(self, bucket_name, public_key, secret_key):
        
        self.session = boto3.Session(
            aws_access_key_id=public_key,
            aws_secret_access_key=secret_key,
        )
        # Let's use Amazon S3
        self.s3 = self.session.client("s3")
        self.bucket_name = bucket_name
        
    async def upload(self, filepath, folder_s3="mspeak"):

        self.s3.upload_file(
            Filename=filepath,
            Bucket=self.bucket_name,
            Key=folder_s3 + "/" + filepath.split("/")[-1],
        ) 

    async def download(self, filename, folder_s3="mspeak", folder_local="../downloaded"):

        meta_data = self.s3.head_object(Bucket=self.bucket_name, 
                                               Key=f"{folder_s3}/{filename}")
        total_length = int(meta_data.get('ContentLength', 0))
        with tqdm(total=total_length,  desc=f'source: s3://{self.bucket_name}/{folder_s3}', 
                  bar_format="{percentage:.1f}%|{bar:25} | {rate_fmt} | {desc}",  
                  unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            with open(f"{folder_local}/{filename}", 'wb') as f:
                self.s3.download_fileobj(self.bucket_name,
                    f"{folder_s3}/{filename}", f, Callback=pbar.update)

s3_saving = S3Connection(os.getenv("AWS_SERVER_BUCKET"), 
                        os.getenv("AWS_SERVER_PUBLIC_KEY"), 
                        os.getenv("AWS_SERVER_SECRET_KEY"))

async def process_batch(list_file, folder, action):

    if action == "upload":
        tasks = []
        for filename in list_file:
            tasks.append(s3_saving.upload(filename, folder))
        await asyncio.gather(*tasks)

    elif action == 'download':
        tasks = []
        zip_files = []
        for filename in list_file:
            p = filename.split("/")
            if ".zip" in p[-1]:
                zip_files.append(filename) 
            tasks.append(s3_saving.download(p[-1], folder, f"{p[0]}/{p[1]}"))
        await asyncio.gather(*tasks)  
        # extract zip file 
        for zip_file in zip_files:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall()

def handel_resource(file_path:str, action: str, s3:str):
    
    list_file = open(file_path, "r").readlines()
    list_file = [filename.split("\n")[0] for filename in list_file]

    if args.action == "download":
        not_exist_file = []
        for filename in list_file:
            if not os.path.exists(filename):
                not_exist_file.append(filename)
        if len(not_exist_file) > 0:
            asyncio.run(process_batch(not_exist_file, s3, action))
    else:
        asyncio.run(process_batch(list_file, args.s3, args.action))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Data management')
    parser.add_argument('--filename', type=str, default="tools/s3_utils/list_resource.txt",
                            help='file_download')
    parser.add_argument('--action', type=str, default="download",
                            help='action download or upload')
    parser.add_argument('--s3', type=str, default="mspeak/resource",
                            help='action download or upload')
    args = parser.parse_args()

    list_file = open(args.filename, "r").readlines()
    list_file = [filename.split("\n")[0] for filename in list_file]

    if args.action == "download":
        not_exist_file = []
        for filename in list_file:
            if not os.path.exists(filename):
                not_exist_file.append(filename)
        if len(not_exist_file) > 0:
            asyncio.run(process_batch(not_exist_file, args.s3, args.action))
    else:
        asyncio.run(process_batch(list_file, args.s3, args.action))
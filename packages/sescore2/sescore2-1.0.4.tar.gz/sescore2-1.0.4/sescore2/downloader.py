import subprocess

def download_from_drive(FILE_ID='1XBfjvNbm5tpxdD62_gVpKQhwwrqXyewt', FILENAME='sescore2_en_supervised_3B.ckpt.ckpt'):
    command = f'''wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id={FILE_ID}' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\\1\\n/p')&id={FILE_ID}" -O {FILENAME} && rm -rf /tmp/cookies.txt'''
    subprocess.run(command, shell=True, check=True)

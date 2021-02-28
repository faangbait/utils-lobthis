#!/home/ss/Development/Repositories/lob-this/venv/bin/python3
# Note - I shebanged this specifically to the location of this project's venv so that I can run it outside of the venv.
# TODO: Change that.

import argparse, sys, os
import lob
import boto3
from botocore.exceptions import ClientError
import secrets

lob.api_key = secrets.TEST_API_KEY

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, os.path.basename(file_name))
    except ClientError as e:
        print("Boto3 error")
        print(e)
        return False
    return True


def lob_letter(file, to_address, from_address=secrets.DEFAULT_FROM, color=False, quiet=False, single_sided=False, test_server=False):
    print(f"Attempting to send {file} to {to_address} from {from_address} with settings c:{color}, q:{quiet}, s:{single_sided}, t: {test_server}...")

    if upload_file(file, secrets.AWS_S3_BUCKET):
        print(f"File uploaded to https://{secrets.AWS_S3_BUCKET}.s3.amazonaws.com/{os.path.basename(file)}")

    if test_server:
        lob.api_key = secrets.TEST_API_KEY
    else:
        lob.api_key = secrets.LIVE_API_KEY

    if single_sided:
        double_sided=False
    else:
        double_sided=True
    try:
        if secrets.DEFAULT_FROM in from_address:
            if test_server:
                lob_from=lob.Address.retrieve(secrets.TEST_SERVER_MY_ADDRESS)
            else:
                lob_from=lob.Address.retrieve(secrets.LIVE_SERVER_MY_ADDRESS)
        else:
            from_address = from_address.split(",")
            lob_from = lob.Address.create(
                name=from_address[0],
                address_line1=from_address[1],
                address_city=from_address[2],
                address_state=from_address[3],
                address_zip=from_address[4]
            )

        to_address=to_address.split(",")
        lob_to = lob.Address.create(
            name=to_address[0],
            address_line1=to_address[1],
            address_city=to_address[2],
            address_state=to_address[3],
            address_zip=to_address[4]
        )

    except Exception as e:
        print(f"error: {e}")
        print("failed to create to/from address")
        sys.exit(1)

    try:
        return lob.Letter.create(
            from_address=lob_from.id,
            to_address=lob_to.id,
            color=color,
            double_sided=double_sided,
            file=f"https://{secrets.AWS_S3_BUCKET}.s3.amazonaws.com/{os.path.basename(file)}",
            address_placement="insert_blank_page"
        )
    except Exception as e:
        print(f"error: {e}")
        print("failed to create lob letter")
        sys.exit(1)

def usage():
    print("Help for Lob")
    print(f"lob.py test.pdf --from {secrets.DEFAULT_FROM} --to John Doe,P.O. Box 1,Dallas,TX,10000 -cqst")
    print("--from\tName, Street Address, City, State, Zip")
    print("--to\tName, Street Address, City, State, Zip")
    print("-c\tin color")
    print("-q\tquietly")
    print("-s\tsingle-sided")
    print("-t\ttest API server")
    print("-h\tthis help file")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send Lob Letters")
    parser.add_argument("file", help="PDF to send")
    parser.add_argument("to_address", help="To Address")
    parser.add_argument("--from_address", help="From Address")
    parser.add_argument("--color",  help="Print in color", action="store_true")
    parser.add_argument("--quiet", help="Work quietly", action="store_true")
    parser.add_argument("--single",  help="Print single-sided", action="store_true")
    parser.add_argument("--test", "-t", help="Use Test API", action="store_true")
    args=parser.parse_args()

    if os.path.exists(args.file):
        file = os.path.abspath(args.file)
    else:
        print("File not found")
        sys.exit(1)

    letter_data = {
        "from_address": args.from_address,
        "color": args.color,
        "quiet": args.quiet,
        "single_sided": args.single,
        "test_server": args.test
    }

    if not letter_data['from_address']:
        letter_data['from_address'] = secrets.DEFAULT_FROM

    try:
        result = lob_letter(file, args.to_address, **letter_data)
        return_msg=f"OK! Your {result['mail_type']} letter will be delivered on {result['expected_delivery_date']}. Proofread it here: {result['url']}"
        if args.test:
            print(f"[TEST API EVENT] {return_msg}")
        else:
            print(return_msg)
    except Exception as e:
        print(e)

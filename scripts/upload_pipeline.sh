echo Enter the EC2 public address.
read EC2_ADDRESS
echo Enter the path to your key.
read KEY_PATH
scp -i $KEY_PATH -r ./pipeline ec2-user@$EC2_ADDRESS:pipeline
scp -i $KEY_PATH -r .env ec2-user@$EC2_ADDRESS:.env
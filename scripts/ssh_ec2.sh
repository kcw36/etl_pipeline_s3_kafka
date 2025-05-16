echo Enter the EC2 public address.
read EC2_ADDRESS
echo Enter the path to your key.
read KEY_PATH
ssh -i $KEY_PATH ec2-user@$EC2_ADDRESS


                 
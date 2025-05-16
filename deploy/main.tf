provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
}

resource "aws_security_group" "db-security-group" {
    name = "museum-db-sg"
    vpc_id = var.CURRENT_VPC_ID
}

resource "aws_vpc_security_group_ingress_rule" "db-sg-inbound-rule" {
    security_group_id = aws_security_group.db-security-group.id
    cidr_ipv4 = "0.0.0.0/0"
    from_port = 5432
    ip_protocol = "tcp"
    to_port = 5432
}

resource "aws_db_instance" "museum-db" {
    allocated_storage = 10
    db_name = var.DATABASE_NAME
    engine = "postgres"
    identifier = "museum-db"
    engine_version = "17.2"
    instance_class = "db.t3.micro"
    publicly_accessible = true
    performance_insights_enabled = false
    skip_final_snapshot = true
    db_subnet_group_name = var.PUBLIC_GROUP_NAME
    vpc_security_group_ids = [aws_security_group.db-security-group.id]
    username = var.DATABASE_USERNAME
    password = var.DATABASE_PASSWORD
}

resource "aws_security_group" "ec2-security-group" {
    name = "museum-ec2-sg"
    vpc_id = var.CURRENT_VPC_ID
}

resource "aws_vpc_security_group_egress_rule" "ec2-sg-outbound-rule" {
    security_group_id = aws_security_group.ec2-security-group.id
    cidr_ipv4 = "0.0.0.0/0"
    from_port = 5432
    ip_protocol = "tcp"
    to_port = 5432
}

resource "aws_vpc_security_group_ingress_rule" "ec2-sg-inbound-rule" {
    security_group_id = aws_security_group.ec2-security-group.id
    cidr_ipv4 = "0.0.0.0/0"
    from_port = 22
    ip_protocol = "tcp"
    to_port = 22
}

resource "aws_vpc_security_group_egress_rule" "ec2-sg-pip-outbound-rule" {
    security_group_id = aws_security_group.ec2-security-group.id
    cidr_ipv4 = "0.0.0.0/0"
    from_port = 443
    ip_protocol = "tcp"
    to_port = 443
}

resource "aws_vpc_security_group_ingress_rule" "ec2-sg-pip-inbound-rule" {
    security_group_id = aws_security_group.ec2-security-group.id
    cidr_ipv4 = "0.0.0.0/0"
    from_port = 443
    ip_protocol = "tcp"
    to_port = 443
}

resource "aws_vpc_security_group_egress_rule" "ec2-sg-kafka-outbound-rule" {
    security_group_id = aws_security_group.ec2-security-group.id
    cidr_ipv4 = "0.0.0.0/0"
    from_port = 9092
    ip_protocol = "tcp"
    to_port = 9092
}

resource "aws_vpc_security_group_ingress_rule" "ec2-sg-kafka-inbound-rule" {
    security_group_id = aws_security_group.ec2-security-group.id
    cidr_ipv4 = "0.0.0.0/0"
    from_port = 9092
    ip_protocol = "tcp"
    to_port = 9092
}

resource "aws_key_pair" "ec2_key_pair" {
  key_name   = "ec2-kp"  
  public_key = file("~/.ssh/ec2_key.pub")
}

resource "aws_instance" "museum_ec2_instance" {
  ami           = "ami-0fc32db49bc3bfbb1"
  instance_type = "t2.nano"              

  subnet_id                   = var.CURRENT_SUBNET_ID
  vpc_security_group_ids      = [aws_security_group.ec2-security-group.id]
  associate_public_ip_address = true

  root_block_device {
    volume_type = "gp3"
    volume_size = 8
  }

  key_name = aws_key_pair.ec2_key_pair.key_name

  tags = {
    Name = "museum-ec2"
  }
}
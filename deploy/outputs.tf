output "rds_address" {
  description = "Public address of RDS instance"
  value = aws_db_instance.museum-db.address
}

output "ec2_address" {
  description = "Public address of EC2 instance"
  value = aws_instance.museum_ec2_instance.public_dns
}
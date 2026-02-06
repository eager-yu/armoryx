import random
from django.core.management.base import BaseCommand
from apps.vpc.models import Vpc


class Command(BaseCommand):
    help = "生成随机的 VPC 记录"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="要生成的记录数量（默认：10）",
        )

    def handle(self, *args, **options):
        count = options["count"]
        
        # 预设的随机数据
        accounts = ["aliyun", "tencent", "aws", "azure", "huawei"]
        regions = ["cn-beijing", "cn-shanghai", "cn-guangzhou", "cn-shenzhen", "us-east-1", "us-west-1"]
        
        # 生成随机 VPC ID
        def generate_vpc_id():
            prefix = random.choice(["vpc-", "vpc_", "vpc"])
            return f"{prefix}{''.join(random.choices('0123456789abcdef', k=12))}"
        
        # 生成随机 VPC 名称
        def generate_vpc_name():
            prefixes = ["production", "development", "testing", "staging", "demo"]
            suffixes = ["vpc", "network", "net"]
            num = random.randint(1, 99)
            return f"{random.choice(prefixes)}-{random.choice(suffixes)}-{num}"
        
        self.stdout.write(f"开始生成 {count} 条 VPC 记录...")
        
        vpcs = []
        vpc_ids = set()
        
        for i in range(count):
            # 确保 VPC ID 唯一
            vpc_id = generate_vpc_id()
            while vpc_id in vpc_ids:
                vpc_id = generate_vpc_id()
            vpc_ids.add(vpc_id)
            
            vpc = Vpc(
                account=random.choice(accounts),
                region=random.choice(regions),
                vpc_id=vpc_id,
                vpc_name=generate_vpc_name(),
            )
            vpcs.append(vpc)
        
        # 批量创建
        Vpc.objects.bulk_create(vpcs)
        
        self.stdout.write(
            self.style.SUCCESS(f"成功生成 {count} 条 VPC 记录！")
        )
        
        # 显示统计信息
        self.stdout.write("\n统计信息：")
        for account in accounts:
            count_by_account = Vpc.objects.filter(account=account).count()
            if count_by_account > 0:
                self.stdout.write(f"  {account}: {count_by_account} 条")
        
        for region in regions:
            count_by_region = Vpc.objects.filter(region=region).count()
            if count_by_region > 0:
                self.stdout.write(f"  {region}: {count_by_region} 条")

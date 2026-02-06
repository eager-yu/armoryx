import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.instances.models import Instance


class Command(BaseCommand):
    help = "生成200条随机的实例记录"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=200,
            help="要生成的记录数量（默认：200）",
        )

    def handle(self, *args, **options):
        count = options["count"]
        
        # 预设的随机数据
        accounts = ["aliyun", "tencent", "aws", "azure", "huawei"]
        regions = ["cn-beijing", "cn-shanghai", "cn-guangzhou", "cn-shenzhen", "us-east-1", "us-west-1"]
        states = ["running", "stopped", "pending", "terminated"]
        
        # 生成随机IP地址
        def generate_ip():
            return f"{random.randint(10, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        # 生成随机实例ID
        def generate_instance_id():
            prefix = random.choice(["i-", "ins-", "ecs-"])
            return f"{prefix}{''.join(random.choices('0123456789abcdef', k=16))}"
        
        # 生成随机实例名称
        def generate_instance_name():
            prefixes = ["web", "db", "app", "cache", "api", "worker", "proxy"]
            suffixes = ["server", "node", "instance", "host", "vm"]
            num = random.randint(1, 999)
            return f"{random.choice(prefixes)}-{random.choice(suffixes)}-{num}"
        
        # 生成随机安全组ID
        def generate_security_group_id():
            return f"sg-{''.join(random.choices('0123456789abcdef', k=12))}"
        
        # 生成随机创建时间（过去30天内）
        def generate_create_time():
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            return timezone.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
        
        self.stdout.write(f"开始生成 {count} 条实例记录...")
        
        instances = []
        instance_ids = set()
        
        for i in range(count):
            # 确保实例ID唯一
            instance_id = generate_instance_id()
            while instance_id in instance_ids:
                instance_id = generate_instance_id()
            instance_ids.add(instance_id)
            
            instance = Instance(
                account=random.choice(accounts),
                region=random.choice(regions),
                instance_id=instance_id,
                instance_name=generate_instance_name(),
                ip=generate_ip(),
                security_groupid=generate_security_group_id(),
                state=random.choice(states),
                create_time=generate_create_time(),
            )
            instances.append(instance)
        
        # 批量创建
        Instance.objects.bulk_create(instances, batch_size=100)
        
        self.stdout.write(
            self.style.SUCCESS(f"成功生成 {count} 条实例记录！")
        )
        
        # 显示统计信息
        self.stdout.write("\n统计信息：")
        for account in accounts:
            count_by_account = Instance.objects.filter(account=account).count()
            self.stdout.write(f"  {account}: {count_by_account} 条")
        
        for state in states:
            count_by_state = Instance.objects.filter(state=state).count()
            self.stdout.write(f"  {state}: {count_by_state} 条")

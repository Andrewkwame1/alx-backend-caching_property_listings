from django.core.management.base import BaseCommand
from properties.models import Property
from properties.utils import get_all_properties, get_redis_cache_metrics
from django.core.cache import cache
import time


class Command(BaseCommand):
    help = 'Test caching functionality'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== Testing Property Caching System ===\n'))

        # Clear any existing cache
        cache.clear()
        self.stdout.write('1. Cleared all cache\n')

        # Create sample properties if none exist
        if Property.objects.count() == 0:
            self.stdout.write('2. Creating sample properties...')
            Property.objects.create(
                title="Luxury Apartment",
                description="Beautiful 2BR apartment in downtown",
                price=250000.00,
                location="New York"
            )
            Property.objects.create(
                title="Beach House",
                description="Stunning ocean view property",
                price=500000.00,
                location="Miami"
            )
            Property.objects.create(
                title="Mountain Cabin",
                description="Cozy cabin in the mountains",
                price=180000.00,
                location="Colorado"
            )
            self.stdout.write(self.style.SUCCESS('   Created 3 properties\n'))
        else:
            self.stdout.write(f'2. Using existing {Property.objects.count()} properties\n')

        # Test cache miss (first call)
        self.stdout.write('3. First call - Should be CACHE MISS:')
        start = time.time()
        properties = get_all_properties()
        elapsed = time.time() - start
        self.stdout.write(f'   Retrieved {len(properties)} properties in {elapsed:.4f} seconds\n')

        # Test cache hit (second call)
        self.stdout.write('4. Second call - Should be CACHE HIT:')
        start = time.time()
        properties = get_all_properties()
        elapsed = time.time() - start
        self.stdout.write(f'   Retrieved {len(properties)} properties in {elapsed:.4f} seconds\n')

        # Show cache metrics
        self.stdout.write('5. Cache Metrics:')
        metrics = get_redis_cache_metrics()
        self.stdout.write(f'   Hits: {metrics["keyspace_hits"]}')
        self.stdout.write(f'   Misses: {metrics["keyspace_misses"]}')
        self.stdout.write(f'   Hit Ratio: {metrics["hit_ratio_percentage"]}%\n')

        # Test cache invalidation
        self.stdout.write('6. Testing cache invalidation...')
        self.stdout.write('   Creating a new property...')
        Property.objects.create(
            title="Test Property",
            description="For testing cache invalidation",
            price=100000.00,
            location="Test City"
        )
        self.stdout.write(self.style.SUCCESS('   Cache should be automatically cleared!\n'))

        # Verify cache was cleared
        self.stdout.write('7. Verifying cache invalidation - Should be CACHE MISS again:')
        start = time.time()
        properties = get_all_properties()
        elapsed = time.time() - start
        self.stdout.write(f'   Retrieved {len(properties)} properties in {elapsed:.4f} seconds\n')

        self.stdout.write(self.style.SUCCESS('\n=== Test Complete! ===\n'))
        self.stdout.write('Expected results:')
        self.stdout.write('- First call: Slower (cache miss, database query)')
        self.stdout.write('- Second call: Much faster (cache hit, no database)')
        self.stdout.write('- After creating property: Slower again (cache cleared, new data)')
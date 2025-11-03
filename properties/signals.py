from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger('properties')

@receiver(post_save, sender=Property)
def invalidate_cache_on_save(sender, instance, created, **kwargs):
    """
    Signal handler that runs AFTER a Property is saved (created or updated).
    
    Think of this like: "Whenever someone adds or changes a property,
    immediately throw away the old cached list because it's now outdated!"
    
    Args:
        sender: The model class (Property)
        instance: The actual property object that was saved
        created: True if this is a new property, False if it was updated
    """
    action = "created" if created else "updated"
    logger.info(f"Property {instance.id} was {action}. Invalidating cache...")
    
    # Delete the cached property list
    cache.delete('all_properties')
    
    logger.info("Cache invalidated successfully")


@receiver(post_delete, sender=Property)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    """
    Signal handler that runs AFTER a Property is deleted.
    
    Similar to above: "Whenever someone deletes a property,
    throw away the old cached list!"
    
    Args:
        sender: The model class (Property)
        instance: The property object that was deleted
    """
    logger.info(f"Property {instance.id} was deleted. Invalidating cache...")
    
    # Delete the cached property list
    cache.delete('all_properties')
    
    logger.info("Cache invalidated successfully")
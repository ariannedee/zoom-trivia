def rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'round{instance.round.number}-question{instance.number}.{ext}'
    return filename

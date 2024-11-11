from datetime import datetime

def time_passed(created_at):
    now = datetime.now()
    diff = now - created_at

    if diff.days > 365:
        years = diff.days // 365
        return f"{years} سال پیش"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} ماه پیش"
    elif diff.days > 0:
        return f"{diff.days} روز پیش"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} ساعت پیش"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} دقیقه پیش"
    else:
        return "لحظاتی پیش"
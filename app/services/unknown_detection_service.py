from datetime import datetime, timedelta


class UnknownDetectionService:

    def __init__(self, cooldown_seconds=10):

        self.cooldown = timedelta(
            seconds=cooldown_seconds
        )

        self.last_alerts = {}

    def notify(
        self,
        camera_id,
        camera_name,
        location,
        track_id
    ):

        now = datetime.now()

        key = (
            camera_id,
            track_id
        )

        last_alert = self.last_alerts.get(key)

        if last_alert is not None:

            if now - last_alert < self.cooldown:

                return False

        self.last_alerts[key] = now

        print("\n" + "=" * 60)
        print("⚠️  ALERTE : PERSONNE INCONNUE DETECTEE")
        print("=" * 60)

        print(f"Caméra       : {camera_name}")
        print(f"Localisation : {location}")
        print(f"Track ID     : {track_id}")
        print(f"Date         : {now.date()}")
        print(f"Heure        : {now.time()}")

        print("=" * 60 + "\n")

        return True
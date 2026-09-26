class TrackIdentityManager:

    def __init__(self):

        # {
        #     track_id: employee_id
        # }
        self.track_identities = {}


    def get_identity(self, track_id):

        return self.track_identities.get(
            track_id
        )


    def set_identity(
        self,
        track_id,
        employee_id
    ):

        self.track_identities[
            track_id
        ] = employee_id


    def remove_track(self, track_id):

        self.track_identities.pop(
            track_id,
            None
        )


    def contains(self, track_id):

        return track_id in self.track_identities


    def get_all(self):

        return self.track_identities.copy()


    def clear(self):

        self.track_identities.clear()
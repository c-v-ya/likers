class EmailHunter:
    # Class mocking EmailHunter.co since you "can't use webmail address", wut?!

    @staticmethod
    def email_valid(email):
        # Instead of this would be a remote request
        # returning True for "result: deliverable"
        if email.endswith('.invalid'):
            return False

        return True

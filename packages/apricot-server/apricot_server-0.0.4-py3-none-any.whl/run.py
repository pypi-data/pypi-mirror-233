import argparse

from apricot import ApricotServer
from apricot.oauth import OAuthBackend

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            prog="Apricot",
            description="Apricot is a proxy for delegating LDAP requests to an OpenID Connect backend.",
        )
        # Common options needed for all backends
        parser.add_argument("-b", "--backend", type=OAuthBackend, help="Which OAuth backend to use.")
        parser.add_argument("-d", "--domain", type=str, help="Which domain users belong to.")
        parser.add_argument("-p", "--port", type=int, default=1389, help="Port to run on.")
        parser.add_argument("-i", "--client-id", type=str, help="OAuth client ID.")
        parser.add_argument("-s", "--client-secret", type=str, help="OAuth client secret.")
        # Options for Microsoft Entra backend
        group = parser.add_argument_group("Microsoft Entra")
        group.add_argument("-t", "--entra-tenant-id", type=str, help="Microsoft Entra tenant ID.", required=False)
        # Parse arguments
        args = parser.parse_args()

        # Create the Apricot server
        reactor = ApricotServer(**vars(args))
    except Exception:
        msg = "Unable to initialise Apricot server from provided command line arguments."
        raise ValueError(msg)

    # Run the Apricot server
    reactor.run()

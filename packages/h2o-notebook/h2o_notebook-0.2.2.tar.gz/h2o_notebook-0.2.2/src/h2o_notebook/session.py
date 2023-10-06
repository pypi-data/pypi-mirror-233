from typing import Callable
from typing import Optional

import h2o_authn
import h2o_discovery

# Name of the platform client in the discovery response.
PLATFORM_CLIENT_NAME = "platform"

class Session:
    def __init__(
            self,
            environment_url: Optional[str] = None,
            config_path: str = None,
            platform_token: Optional[str] = None,
            token_provider: Callable[[], str] = None,
    ) -> None:
        """Initializes session.

        :param environment_url: Override for the URL of the environment passed to the discovery service.
        :param config_path: Override path to the h2o cli config file passed to the discovery service.
        :param platform_token: Platform token. If not provided, the token will be discovered.
        :param token_provider: Token provider. If not provided, the provider will be constructed from the discovered config.
        """
        if token_provider is not None:
            # Test token refresh
            token_provider()
            self.token_provider = token_provider
            return

        # Discover connection configuration
        d = h2o_discovery.discover(environment=environment_url, config_path=config_path)

        # Discover platform_token if not provided
        if not platform_token:
            platform_token = d.credentials[PLATFORM_CLIENT_NAME].refresh_token

        # Discover client id
        client_id = d.clients.get(PLATFORM_CLIENT_NAME).oauth2_client_id
        if not client_id:
            raise ConnectionError(
                "Unable to discover platform oauth2_client_id connection value."
            )

        # Initialize token provider
        token_provider = h2o_authn.TokenProvider(
            issuer_url=d.environment.issuer_url,
            client_id=client_id,
            refresh_token=platform_token,
        )
        # Test token refresh
        token_provider()

        self.token_provider = token_provider

    def get_token_provider(self) -> Callable[[], str]:
        """Returns token provider."""
        return self.token_provider

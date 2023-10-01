from predeployed_generator.upgradeable_contract_generator import UpgradeableContractGenerator

from .token_manager import TokenManagerGenerator


class TokenManagerErc20Generator(TokenManagerGenerator):
    ARTIFACT_FILENAME = "TokenManagerERC20.json"
    META_FILENAME = "TokenManagerERC20.meta.json"

    # ---------- storage ----------
    # --------Initializable--------
    # 0:    _initialized, _initializing;
    # -----ContextUpgradeable------
    # 1:    __gap
    # ...   __gap
    # 50:   __gap
    # ------ERC165Upgradeable------
    # 51:   __gap
    # ...   __gap
    # 100:  __gap
    # --AccessControlUpgradeable---
    # 101:  _roles
    # 102:  __gap
    # ...   __gap
    # 150:  __gap
    # AccessControlEnumerableUpgradeable
    # 151:  _roleMembers
    # 152:  __gap
    # ...   __gap
    # 200:  __gap
    # ---------TokenManager---------
    # 201:  messageProxy
    # 202:  tokenManagerLinker
    # 203:  communityLocker
    # 204:  schainHash
    # 205:  depositBox, automaticDeploy
    # 206:  tokenManagers
    # ------TokenManagerERC20------
    # 207:  clonesErc20
    # 208:  totalSupplyOnMainnet

    def __init__(self):
        super().__init__()


class UpgradeableTokenManagerErc20Generator(UpgradeableContractGenerator):
    """Generates upgradeable instance of TokenManagerErc20Upgradeable
    """

    def __init__(self):
        super().__init__(implementation_generator=TokenManagerErc20Generator())

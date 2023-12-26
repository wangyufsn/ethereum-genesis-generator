from web3.auto import w3
import json
import ruamel.yaml as yaml
import sys
import os

w3.eth.account.enable_unaudited_hdwallet_features()

testnet_config_path = "genesis-config.yaml"
mainnet_config_path = "/apps/el-gen/mainnet/chainspec.json"
sepolia_config_path = "/apps/el-gen/sepolia/chainspec.json"
goerli_config_path = "/apps/el-gen/goerli/chainspec.json"
holesky_config_path = "/apps/el-gen/holesky/chainspec.json"

validator_balance = "1638400" + '0' * 18

if len(sys.argv) > 1:
    testnet_config_path = sys.argv[1]
    # Get the directory of the config file
    testnet_config_dir = os.path.dirname(testnet_config_path)
    allocs_path = testnet_config_dir + "/allocs.json"

with open(testnet_config_path) as stream:
    data = yaml.safe_load(stream)

if int(data['chain_id']) == 1:
    with open(mainnet_config_path) as m:
        mainnet_json = json.loads(m.read())
    out = mainnet_json
elif int(data['chain_id']) == 5:
    with open(goerli_config_path) as m:
        goerli_json = json.loads(m.read())
    out = goerli_json
elif int(data['chain_id']) == 11155111:
    with open(sepolia_config_path) as m:
        sepolia_json = json.loads(m.read())
    out = sepolia_json
elif int(data['chain_id']) == 17000:
    with open(holesky_config_path) as m:
        holesky_json = json.loads(m.read())
    out = holesky_json
else:
    out = {
        "name": "Testnet",
        "engine": {},
        "params": {
            "gasLimitBoundDivisor": "0x400",
            "registrar": "0x0000000000000000000000000000000000000000",
            "accountStartNonce": "0x0",
            "maximumExtraDataSize": "0xffff",
            "minGasLimit": "0x1388",
            "networkID": hex(int(data['chain_id'])),
            "MergeForkIdTransition": "0x0",
            "maxCodeSize": "0x6000",
            "maxCodeSizeTransition": "0x0",
            "eip150Transition": "0x0",
            "eip158Transition": "0x0",
            "eip160Transition": "0x0",
            "eip161abcTransition": "0x0",
            "eip161dTransition": "0x0",
            "eip155Transition": "0x0",
            "eip140Transition": "0x0",
            "eip211Transition": "0x0",
            "eip214Transition": "0x0",
            "eip658Transition": "0x0",
            "eip145Transition": "0x0",
            "eip1014Transition": "0x0",
            "eip1052Transition": "0x0",
            "eip1283Transition": "0x0",
            "eip1283DisableTransition": "0x0",
            "eip152Transition": "0x0",
            "eip1108Transition": "0x0",
            "eip1344Transition": "0x0",
            "eip1884Transition": "0x0",
            "eip2028Transition": "0x0",
            "eip2200Transition": "0x0",
            "eip2565Transition": "0x0",
            "eip2929Transition": "0x0",
            "eip2930Transition": "0x0",
            "eip1559Transition": "0x0",
            "eip3198Transition": "0x0",
            "eip3529Transition": "0x0",
            "eip3541Transition": "0x0",
            "eip4895TransitionTimestamp": hex(int(data['genesis_timestamp']) + int(data['genesis_delay'])),
            "eip3855TransitionTimestamp": hex(int(data['genesis_timestamp']) + int(data['genesis_delay'])),
            "eip3651TransitionTimestamp": hex(int(data['genesis_timestamp']) + int(data['genesis_delay'])),
            "eip3860TransitionTimestamp": hex(int(data['genesis_timestamp']) + int(data['genesis_delay'])),
            "terminalTotalDifficulty":"0x0"
        },
        "genesis": {
            "seal": {
                "ethereum": {
                    "nonce": "0x1234",
                    "mixHash": "0x0000000000000000000000000000000000000000000000000000000000000000"
                }
            },
            "difficulty": "0x01",
            "author": "0x0000000000000000000000000000000000000000",
            "timestamp": hex(data['genesis_timestamp']),
            "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
            "extraData": "",
            "gasLimit": "0x17D7840"
        },
        "accounts": {
            # Allocate 1 wei to all possible pre-compiles.
            # See https://github.com/ethereum/EIPs/issues/716 "SpuriousDragon RIPEMD bug"
            # E.g. Rinkeby allocates it like this.
            # See https://github.com/ethereum/go-ethereum/blob/092856267067dd78b527a773f5b240d5c9f5693a/core/genesis.go#L370
            **{
                "0x" + i.to_bytes(length=20, byteorder='big').hex(): {
                    "balance": "1",
                } for i in [x for x in range(256) if x != 11]
            },
            data['deposit_contract_address']: {
                "balance": validator_balance,
                "code": "0x60806040526004361061003f5760003560e01c806301ffc9a71461004457806322895118146100a4578063621fd130146101ba578063c5f2892f14610244575b600080fd5b34801561005057600080fd5b506100906004803603602081101561006757600080fd5b50357fffffffff000000000000000000000000000000000000000000000000000000001661026b565b604080519115158252519081900360200190f35b6101b8600480360360808110156100ba57600080fd5b8101906020810181356401000000008111156100d557600080fd5b8201836020820111156100e757600080fd5b8035906020019184600183028401116401000000008311171561010957600080fd5b91939092909160208101903564010000000081111561012757600080fd5b82018360208201111561013957600080fd5b8035906020019184600183028401116401000000008311171561015b57600080fd5b91939092909160208101903564010000000081111561017957600080fd5b82018360208201111561018b57600080fd5b803590602001918460018302840111640100000000831117156101ad57600080fd5b919350915035610304565b005b3480156101c657600080fd5b506101cf6110b5565b6040805160208082528351818301528351919283929083019185019080838360005b838110156102095781810151838201526020016101f1565b50505050905090810190601f1680156102365780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561025057600080fd5b506102596110c7565b60408051918252519081900360200190f35b60007fffffffff0000000000000000000000000000000000000000000000000000000082167f01ffc9a70000000000000000000000000000000000000000000000000000000014806102fe57507fffffffff0000000000000000000000000000000000000000000000000000000082167f8564090700000000000000000000000000000000000000000000000000000000145b92915050565b6030861461035d576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001806118056026913960400191505060405180910390fd5b602084146103b6576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252603681526020018061179c6036913960400191505060405180910390fd5b6060821461040f576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260298152602001806118786029913960400191505060405180910390fd5b670de0b6b3a7640000341015610470576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001806118526026913960400191505060405180910390fd5b633b9aca003406156104cd576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260338152602001806117d26033913960400191505060405180910390fd5b633b9aca00340467ffffffffffffffff811115610535576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252602781526020018061182b6027913960400191505060405180910390fd5b6060610540826114ba565b90507f649bbc62d0e31342afea4e5cd82d4049e7e1ee912fc0889aa790803be39038c589898989858a8a6105756020546114ba565b6040805160a0808252810189905290819060208201908201606083016080840160c085018e8e80828437600083820152601f017fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe01690910187810386528c815260200190508c8c808284376000838201819052601f9091017fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe01690920188810386528c5181528c51602091820193918e019250908190849084905b83811015610648578181015183820152602001610630565b50505050905090810190601f1680156106755780820380516001836020036101000a031916815260200191505b5086810383528881526020018989808284376000838201819052601f9091017fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0169092018881038452895181528951602091820193918b019250908190849084905b838110156106ef5781810151838201526020016106d7565b50505050905090810190601f16801561071c5780820380516001836020036101000a031916815260200191505b509d505050505050505050505050505060405180910390a1600060028a8a600060801b604051602001808484808284377fffffffffffffffffffffffffffffffff0000000000000000000000000000000090941691909301908152604080517ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0818403018152601090920190819052815191955093508392506020850191508083835b602083106107fc57805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe090920191602091820191016107bf565b51815160209384036101000a7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff01801990921691161790526040519190930194509192505080830381855afa158015610859573d6000803e3d6000fd5b5050506040513d602081101561086e57600080fd5b5051905060006002806108846040848a8c6116fe565b6040516020018083838082843780830192505050925050506040516020818303038152906040526040518082805190602001908083835b602083106108f857805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe090920191602091820191016108bb565b51815160209384036101000a7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff01801990921691161790526040519190930194509192505080830381855afa158015610955573d6000803e3d6000fd5b5050506040513d602081101561096a57600080fd5b5051600261097b896040818d6116fe565b60405160009060200180848480828437919091019283525050604080518083038152602092830191829052805190945090925082918401908083835b602083106109f457805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe090920191602091820191016109b7565b51815160209384036101000a7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff01801990921691161790526040519190930194509192505080830381855afa158015610a51573d6000803e3d6000fd5b5050506040513d6020811015610a6657600080fd5b5051604080516020818101949094528082019290925280518083038201815260609092019081905281519192909182918401908083835b60208310610ada57805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe09092019160209182019101610a9d565b51815160209384036101000a7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff01801990921691161790526040519190930194509192505080830381855afa158015610b37573d6000803e3d6000fd5b5050506040513d6020811015610b4c57600080fd5b50516040805160208101858152929350600092600292839287928f928f92018383808284378083019250505093505050506040516020818303038152906040526040518082805190602001908083835b60208310610bd957805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe09092019160209182019101610b9c565b51815160209384036101000a7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff01801990921691161790526040519190930194509192505080830381855afa158015610c36573d6000803e3d6000fd5b5050506040513d6020811015610c4b57600080fd5b50516040518651600291889160009188916020918201918291908601908083835b60208310610ca957805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe09092019160209182019101610c6c565b6001836020036101000a0380198251168184511680821785525050505050509050018367ffffffffffffffff191667ffffffffffffffff1916815260180182815260200193505050506040516020818303038152906040526040518082805190602001908083835b60208310610d4e57805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe09092019160209182019101610d11565b51815160209384036101000a7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff01801990921691161790526040519190930194509192505080830381855afa158015610dab573d6000803e3d6000fd5b5050506040513d6020811015610dc057600080fd5b5051604080516020818101949094528082019290925280518083038201815260609092019081905281519192909182918401908083835b60208310610e3457805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe09092019160209182019101610df7565b51815160209384036101000a7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff01801990921691161790526040519190930194509192505080830381855afa158015610e91573d6000803e3d6000fd5b5050506040513d6020811015610ea657600080fd5b50519050858114610f02576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260548152602001806117486054913960600191505060405180910390fd5b60205463ffffffff11610f60576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260218152602001806117276021913960400191505060405180910390fd5b602080546001019081905560005b60208110156110a9578160011660011415610fa0578260008260208110610f9157fe5b0155506110ac95505050505050565b600260008260208110610faf57fe5b01548460405160200180838152602001828152602001925050506040516020818303038152906040526040518082805190602001908083835b6020831061102557805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe09092019160209182019101610fe8565b51815160209384036101000a7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff01801990921691161790526040519190930194509192505080830381855afa158015611082573d6000803e3d6000fd5b5050506040513d602081101561109757600080fd5b50519250600282049150600101610f6e565b50fe5b50505050505050565b60606110c26020546114ba565b905090565b6020546000908190815b60208110156112f05781600116600114156111e6576002600082602081106110f557fe5b01548460405160200180838152602001828152602001925050506040516020818303038152906040526040518082805190602001908083835b6020831061116b57805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0909201916020918201910161112e565b51815160209384036101000a7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff01801990921691161790526040519190930194509192505080830381855afa1580156111c8573d6000803e3d6000fd5b5050506040513d60208110156111dd57600080fd5b505192506112e2565b600283602183602081106111f657fe5b015460405160200180838152602001828152602001925050506040516020818303038152906040526040518082805190602001908083835b6020831061126b57805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0909201916020918201910161122e565b51815160209384036101000a7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff01801990921691161790526040519190930194509192505080830381855afa1580156112c8573d6000803e3d6000fd5b5050506040513d60208110156112dd57600080fd5b505192505b6002820491506001016110d1565b506002826112ff6020546114ba565b600060401b6040516020018084815260200183805190602001908083835b6020831061135a57805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0909201916020918201910161131d565b51815160209384036101000a7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff01801990921691161790527fffffffffffffffffffffffffffffffffffffffffffffffff000000000000000095909516920191825250604080518083037ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8018152601890920190819052815191955093508392850191508083835b6020831061143f57805182527fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe09092019160209182019101611402565b51815160209384036101000a7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff01801990921691161790526040519190930194509192505080830381855afa15801561149c573d6000803e3d6000fd5b5050506040513d60208110156114b157600080fd5b50519250505090565b60408051600880825281830190925260609160208201818036833701905050905060c082901b8060071a60f81b826000815181106114f457fe5b60200101907effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916908160001a9053508060061a60f81b8260018151811061153757fe5b60200101907effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916908160001a9053508060051a60f81b8260028151811061157a57fe5b60200101907effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916908160001a9053508060041a60f81b826003815181106115bd57fe5b60200101907effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916908160001a9053508060031a60f81b8260048151811061160057fe5b60200101907effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916908160001a9053508060021a60f81b8260058151811061164357fe5b60200101907effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916908160001a9053508060011a60f81b8260068151811061168657fe5b60200101907effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916908160001a9053508060001a60f81b826007815181106116c957fe5b60200101907effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916908160001a90535050919050565b6000808585111561170d578182fd5b83861115611719578182fd5b505082019391909203915056fe4465706f736974436f6e74726163743a206d65726b6c6520747265652066756c6c4465706f736974436f6e74726163743a207265636f6e7374727563746564204465706f7369744461746120646f6573206e6f74206d6174636820737570706c696564206465706f7369745f646174615f726f6f744465706f736974436f6e74726163743a20696e76616c6964207769746864726177616c5f63726564656e7469616c73206c656e6774684465706f736974436f6e74726163743a206465706f7369742076616c7565206e6f74206d756c7469706c65206f6620677765694465706f736974436f6e74726163743a20696e76616c6964207075626b6579206c656e6774684465706f736974436f6e74726163743a206465706f7369742076616c756520746f6f20686967684465706f736974436f6e74726163743a206465706f7369742076616c756520746f6f206c6f774465706f736974436f6e74726163743a20696e76616c6964207369676e6174757265206c656e677468a26469706673582212201dd26f37a621703009abf16e77e69c93dc50c79db7f6cc37543e3e0e3decdc9764736f6c634300060b0033",
                # "storage": {
                #     "0x0000000000000000000000000000000000000000000000000000000000000022": "0xf5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b",
                #     "0x0000000000000000000000000000000000000000000000000000000000000023": "0xdb56114e00fdd4c1f85c892bf35ac9a89289aaecb1ebd0a96cde606a748b5d71",
                #     "0x0000000000000000000000000000000000000000000000000000000000000024": "0xc78009fdf07fc56a11f122370658a353aaa542ed63e44c4bc15ff4cd105ab33c",
                #     "0x0000000000000000000000000000000000000000000000000000000000000025": "0x536d98837f2dd165a55d5eeae91485954472d56f246df256bf3cae19352a123c",
                #     "0x0000000000000000000000000000000000000000000000000000000000000026": "0x9efde052aa15429fae05bad4d0b1d7c64da64d03d7a1854a588c2cb8430c0d30",
                #     "0x0000000000000000000000000000000000000000000000000000000000000027": "0xd88ddfeed400a8755596b21942c1497e114c302e6118290f91e6772976041fa1",
                #     "0x0000000000000000000000000000000000000000000000000000000000000028": "0x87eb0ddba57e35f6d286673802a4af5975e22506c7cf4c64bb6be5ee11527f2c",
                #     "0x0000000000000000000000000000000000000000000000000000000000000029": "0x26846476fd5fc54a5d43385167c95144f2643f533cc85bb9d16b782f8d7db193",
                #     "0x000000000000000000000000000000000000000000000000000000000000002a": "0x506d86582d252405b840018792cad2bf1259f1ef5aa5f887e13cb2f0094f51e1",
                #     "0x000000000000000000000000000000000000000000000000000000000000002b": "0xffff0ad7e659772f9534c195c815efc4014ef1e1daed4404c06385d11192e92b",
                #     "0x000000000000000000000000000000000000000000000000000000000000002c": "0x6cf04127db05441cd833107a52be852868890e4317e6a02ab47683aa75964220",
                #     "0x000000000000000000000000000000000000000000000000000000000000002d": "0xb7d05f875f140027ef5118a2247bbb84ce8f2f0f1123623085daf7960c329f5f",
                #     "0x000000000000000000000000000000000000000000000000000000000000002e": "0xdf6af5f5bbdb6be9ef8aa618e4bf8073960867171e29676f8b284dea6a08a85e",
                #     "0x000000000000000000000000000000000000000000000000000000000000002f": "0xb58d900f5e182e3c50ef74969ea16c7726c549757cc23523c369587da7293784",
                #     "0x0000000000000000000000000000000000000000000000000000000000000030": "0xd49a7502ffcfb0340b1d7885688500ca308161a7f96b62df9d083b71fcc8f2bb",
                #     "0x0000000000000000000000000000000000000000000000000000000000000031": "0x8fe6b1689256c0d385f42f5bbe2027a22c1996e110ba97c171d3e5948de92beb",
                #     "0x0000000000000000000000000000000000000000000000000000000000000032": "0x8d0d63c39ebade8509e0ae3c9c3876fb5fa112be18f905ecacfecb92057603ab",
                #     "0x0000000000000000000000000000000000000000000000000000000000000033": "0x95eec8b2e541cad4e91de38385f2e046619f54496c2382cb6cacd5b98c26f5a4",
                #     "0x0000000000000000000000000000000000000000000000000000000000000034": "0xf893e908917775b62bff23294dbbe3a1cd8e6cc1c35b4801887b646a6f81f17f",
                #     "0x0000000000000000000000000000000000000000000000000000000000000035": "0xcddba7b592e3133393c16194fac7431abf2f5485ed711db282183c819e08ebaa",
                #     "0x0000000000000000000000000000000000000000000000000000000000000036": "0x8a8d7fe3af8caa085a7639a832001457dfb9128a8061142ad0335629ff23ff9c",
                #     "0x0000000000000000000000000000000000000000000000000000000000000037": "0xfeb3c337d7a51a6fbf00b9e34c52e1c9195c969bd4e7a0bfd51d5c5bed9c1167",
                #     "0x0000000000000000000000000000000000000000000000000000000000000038": "0xe71f0aa83cc32edfbefa9f4d3e0174ca85182eec9f3a09f6a6c0df6377a510d7",
                #     "0x0000000000000000000000000000000000000000000000000000000000000039": "0x31206fa80a50bb6abe29085058f16212212a60eec8f049fecb92d8c8e0a84bc0",
                #     "0x000000000000000000000000000000000000000000000000000000000000003a": "0x21352bfecbeddde993839f614c3dac0a3ee37543f9b412b16199dc158e23b544",
                #     "0x000000000000000000000000000000000000000000000000000000000000003b": "0x619e312724bb6d7c3153ed9de791d764a366b389af13c58bf8a8d90481a46765",
                #     "0x000000000000000000000000000000000000000000000000000000000000003c": "0x7cdd2986268250628d0c10e385c58c6191e6fbe05191bcc04f133f2cea72c1c4",
                #     "0x000000000000000000000000000000000000000000000000000000000000003d": "0x848930bd7ba8cac54661072113fb278869e07bb8587f91392933374d017bcbe1",
                #     "0x000000000000000000000000000000000000000000000000000000000000003e": "0x8869ff2c22b28cc10510d9853292803328be4fb0e80495e8bb8d271f5b889636",
                #     "0x000000000000000000000000000000000000000000000000000000000000003f": "0xb5fe28e79f1b850f8658246ce9b6a1e7b49fc06db7143e8fe0b4f2b0c5523a5c",
                #     "0x0000000000000000000000000000000000000000000000000000000000000040": "0x985e929f70af28d0bdd1a90a808f977f597c7c778c489e98d3bd8910d31ac0f7"
                # }
            }
        },
        "nodes": []
    }

    out["engine"]["Ethash"] =  {}

    for key, value in data['el_premine'].items():
        acct = w3.eth.account.from_mnemonic(data['mnemonic'], account_path=key, passphrase='')
        weival = value.replace('ETH', '0' * 18)
        out["accounts"][acct.address] = {"balance": weival}

    # Some hardcoded addrs
    for addr, account in data['el_premine_addrs'].items():
        # Convert balance format
        if isinstance(account, dict) and 'balance' in account:
            balance_value = account['balance'].replace('ETH', '0' * 18)
        else:
            # If it's not a dictionary, assume it's a single value for backward compatibility
            balance_value = account.replace('ETH', '0' * 18)

        # Create alloc dictionary entry
        alloc_entry = {"balance": balance_value}

        # Optionally add code
        if 'code' in account:
            alloc_entry['code'] = account['code']

        # Optionally add storage
        if 'storage' in account:
            alloc_entry['storage'] = account['storage']

        # Optionally set nonce
        if 'nonce' in account:
            alloc_entry['nonce'] = account['nonce']

        # Optionally set private key
        if 'secretKey' in account:
            alloc_entry['secretKey'] = account['secretKey']

        # Add alloc entry to output's alloc field
        out["accounts"][addr] = alloc_entry

    # If allocs.json exists, add those allocs to the genesis file
    allocs = {}
    try:
        with open(allocs_path) as allocs_file:
            allocs = json.load(allocs_file)
    except FileNotFoundError:
        allocs = {}
        print("No allocs.json file found, skipping...", file=sys.stderr)

    # Add allocs to genesis file
    out["accounts"].update(allocs)

out['params']['eip4844TransitionTimestamp']= hex(int(data['genesis_timestamp']) + int(data['genesis_delay']) + (int(data['deneb_fork_epoch']) * 32 * int(data['slot_duration_in_seconds'])))
out['params']['eip4788TransitionTimestamp']= hex(int(data['genesis_timestamp']) + int(data['genesis_delay']) + (int(data['deneb_fork_epoch']) * 32 * int(data['slot_duration_in_seconds'])))
out['params']['eip1153TransitionTimestamp']= hex(int(data['genesis_timestamp']) + int(data['genesis_delay']) + (int(data['deneb_fork_epoch']) * 32 * int(data['slot_duration_in_seconds'])))
out['params']['eip5656TransitionTimestamp']= hex(int(data['genesis_timestamp']) + int(data['genesis_delay']) + (int(data['deneb_fork_epoch']) * 32 * int(data['slot_duration_in_seconds'])))
out['params']['eip6780TransitionTimestamp']= hex(int(data['genesis_timestamp']) + int(data['genesis_delay']) + (int(data['deneb_fork_epoch']) * 32 * int(data['slot_duration_in_seconds'])))

print(json.dumps(out, indent='  '))

import yaml
class ReqGenerator:
    PROVIDERS = {
        'aws',
        'gcp',
        'azure'
    }
    prov_data = {}
    def __init__(self, providers: list[str]) -> None:
        for prov_id in providers:
            if prov_id in self.PROVIDERS:
                with open(f'../../assets/provider_reqs/{prov_id}.yaml', 'r') as file:
                    self.prov_data[prov_id] = yaml.safe_load(file)
# from d3a.models.appliance.simple import SimpleAppliance
from d3a.models.appliance.switchable import SwitchableAppliance
from d3a.models.area import Area
from d3a.models.strategy.storage import StorageStrategy
from d3a.models.appliance.pv import PVAppliance
from d3a.models.strategy.pv import PVStrategy
from d3a.models.strategy.predefined_load import DefinedLoadStrategy
from d3a.models.strategy.finite_power_plant import FinitePowerPlant
from d3a.models.strategy.predefined_pv import d3a_path
import os




def get_setup(config):
    area = Area(
        'Grid',
        [
            Area(
                'House 1',
                [
                    Area('H1 General Load',
                         strategy=DefinedLoadStrategy(
                             daily_load_profile=os.path.join(d3a_path,
                                                             'resources', 'SAM_MF2_Summer_converted.csv'),
                             acceptable_energy_rate=35),
                         appliance=SwitchableAppliance()),

                    Area('H1 Storage1', strategy=StorageStrategy(initial_capacity=1.2),
                         appliance=SwitchableAppliance()),

                    Area('H1 PV', strategy=PVStrategy(10, 80),
                         appliance=PVAppliance()),

                    Area('H1 Storage2', strategy=StorageStrategy(initial_capacity=0.6),
                         appliance=SwitchableAppliance()),

                ]
            ),
            # Area(
            #     'House 2',
            #     [
            #         Area('H2 General Load', strategy=LoadHoursStrategy(avg_power_W=200,
            #                                                            hrs_per_day=4,
            #                                                            hrs_of_day=list(
            #                                                                range(12, 16)),
            #                                                            acceptable_energy_rate=35),
            #              appliance=SwitchableAppliance()),
            #         Area('H2 PV', strategy=PVStrategy(4, 80),
            #              appliance=PVAppliance()),
            #
            #     ]
            # ),

            # Area(
            #     'Cell Tower', strategy=CellTowerLoadHoursStrategy(avg_power_W=100,
            #                                                        hrs_per_day=24,
            #                                                        hrs_of_day=list(range(0, 24)),
            #                                                        acceptable_energy_rate=35),
            #             appliance=SwitchableAppliance())

        ],
        config=config
    )
    return area

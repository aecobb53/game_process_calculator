from ast import main
from calendar import c
from platform import machine
from pydantic import BaseModel, model_validator
from typing import Any, List, Dict, Optional


class FactorioDataItemBase(BaseModel):
    filename: str
    name: str
    localised_name: List
    project_uid: str
    notes: str | None = None

    def return_base_record(self):
        content = {
            "name": self.name,
            "project_uid": self.project_uid,
            "notes": self.notes,
        }
        return content

    def json_out(self):
        content = {
            'filename': self.filename,
            'name': self.name,
            'localised_name': self.localised_name,
            'project_uid': self.project_uid,
            'notes': self.notes,
        }
        return content

class EnergySource(BaseModel):
    electric: Dict | None = None
    burner: Dict | None = None

    def json_out(self):
        content = {
            'electric': self.electric,
            'burner': self.burner,
        }
        return content


class FactorioDataItem(FactorioDataItemBase):
    type: str | None = None
    order: str
    fuel_value: int
    stack_size: int | None = None
    place_result: str | None = None
    default_temperature: float | None = None
    max_temperature: float | None = None
    emissions_multiplier: float | None = None
    rocket_launch_products: List | None = None
    fuel_category: str | None = None
    fuel_acceleration_multiplier: float | None = None
    fuel_top_speed_multiplier: float | None = None
    burnt_result: str | None = None
    equipment_grid: str | None = None
    place_as_equipment_result: str | None = None
    attack_parameters: Dict | None = None
    category: str | None = None
    tier: int | None = None
    module_effects: Dict | None = None
    limitations: Dict | List | None = None

    resource_uid: str | None = None
    """
    Files:
        items.json
        fluid.json
    """

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        assumed_keys = [
            'project_uid',
            'filename',
            'name',
            'localised_name',
            'type',
            'order',
            'fuel_value',
            'stack_size',
            'place_result',
            'default_temperature',
            'max_temperature',
            'emissions_multiplier',
            'rocket_launch_products',
            'fuel_category',
            'fuel_acceleration_multiplier',
            'fuel_top_speed_multiplier',
            'burnt_result',
            'equipment_grid',
            'place_as_equipment_result',
            'attack_parameters',
            'category',
            'tier',
            'module_effects',
            'limitations',
        ]
        missing_keys = []
        for i in fields.keys():
            if i not in assumed_keys:
                missing_keys.append(i)
        if missing_keys:
            raise ValueError(f"Keys not found in assumed_keys: {missing_keys}")
        return fields

    def return_resource(self):
        content = super().return_base_record()
        # content["name"] = self.name
        return content

    def json_out(self):
        content = super().json_out()
        content['type'] = self.type
        content['order'] = self.order
        content['fuel_value'] = self.fuel_value
        content['stack_size'] = self.stack_size
        content['place_result'] = self.place_result
        content['default_temperature'] = self.default_temperature
        content['max_temperature'] = self.max_temperature
        content['emissions_multiplier'] = self.emissions_multiplier
        content['rocket_launch_products'] = self.rocket_launch_products
        content['fuel_category'] = self.fuel_category
        content['fuel_acceleration_multiplier'] = self.fuel_acceleration_multiplier
        content['fuel_top_speed_multiplier'] = self.fuel_top_speed_multiplier
        content['burnt_result'] = self.burnt_result
        content['equipment_grid'] = self.equipment_grid
        content['place_as_equipment_result'] = self.place_as_equipment_result
        content['attack_parameters'] = self.attack_parameters
        content['category'] = self.category
        content['tier'] = self.tier
        content['module_effects'] = self.module_effects
        content['limitations'] = self.limitations

        content['resource_uid'] = self.resource_uid
        return content


class FactorioDataMachine(FactorioDataItemBase):
    type: str | None = None
    energy_usage: int | None = None
    ingredient_count: int | None = None
    crafting_speed: float | None = None
    crafting_categories: Dict | None = None
    module_inventory_size: int | None = None
    allowed_effects: Dict | None = None
    friendly_map_color: Dict
    enemy_map_color: Dict
    energy_source: EnergySource
    pollution: float
    max_energy_usage: int | None = None
    target_temperature: int | None = None
    input_fluid: str | None = None
    output_fluid: str | None = None
    maximum_temperature: int | None = None
    effectivity: float | None = None
    fluid_usage_per_tick: float | None = None
    max_energy_production: int | None = None
    lab_inputs: List | None = None
    researching_speed: float | None = None
    mining_speed: float | None = None
    resource_categories: Dict | None = None
    neighbour_bonus: float | None = None
    fixed_recipe: str | None = None
    rocket_parts_required: int | None = None
    """
    Files:
        assembling-machine.json
        boiler.json
        furnace.json
        generator.json
        lab.json
        mining-drill.json
        reactor.json
        rocket-silo.json
        solar-panel.json
    """

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        assumed_keys = [
            'project_uid',
            'filename',
            'name',
            'localised_name',
            'type',
            'energy_usage',
            'ingredient_count',
            'crafting_speed',
            'crafting_categories',
            'module_inventory_size',
            'allowed_effects',
            'friendly_map_color',
            'enemy_map_color',
            'energy_source',
            'pollution',
            'max_energy_usage',
            'target_temperature',
            'input_fluid',
            'output_fluid',
            'maximum_temperature',
            'effectivity',
            'fluid_usage_per_tick',
            'max_energy_production',
            'lab_inputs',
            'researching_speed',
            'mining_speed',
            'resource_categories',
            'neighbour_bonus',
            'fixed_recipe',
            'rocket_parts_required',
        ]
        missing_keys = []
        for i in fields.keys():
            if i not in assumed_keys:
                missing_keys.append(i)
        if missing_keys:
            raise ValueError(f"Keys not found in assumed_keys: {missing_keys}")
        return fields

    def json_out(self):
        content = super().json_out()
        content['type'] = self.type
        content['energy_usage'] = self.energy_usage
        content['ingredient_count'] = self.ingredient_count
        content['crafting_speed'] = self.crafting_speed
        content['crafting_categories'] = self.crafting_categories
        content['module_inventory_size'] = self.module_inventory_size
        content['allowed_effects'] = self.allowed_effects
        content['friendly_map_color'] = self.friendly_map_color
        content['enemy_map_color'] = self.enemy_map_color
        content['energy_source'] = self.energy_source.json_out()
        content['pollution'] = self.pollution
        content['max_energy_usage'] = self.max_energy_usage
        content['target_temperature'] = self.target_temperature
        content['input_fluid'] = self.input_fluid
        content['output_fluid'] = self.output_fluid
        content['maximum_temperature'] = self.maximum_temperature
        content['effectivity'] = self.effectivity
        content['fluid_usage_per_tick'] = self.fluid_usage_per_tick
        content['max_energy_production'] = self.max_energy_production
        content['lab_inputs'] = self.lab_inputs
        content['researching_speed'] = self.researching_speed
        content['mining_speed'] = self.mining_speed
        content['resource_categories'] = self.resource_categories
        content['neighbour_bonus'] = self.neighbour_bonus
        content['fixed_recipe'] = self.fixed_recipe
        content['rocket_parts_required'] = self.rocket_parts_required
        return content

class FactorioDataLogistics(FactorioDataItemBase):
    max_energy_usage: int | None = None
    inserter_extension_speed: float | None = None
    inserter_rotation_speed: float | None = None
    friendly_map_color: Dict
    enemy_map_color: Dict
    energy_source: EnergySource | None = None
    pollution: float | None = None
    belt_speed: float | None = None
    """
    Files:
        inserter.json
        transport-belt.json
    """

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        assumed_keys = [
            'project_uid',
            'filename',
            'name',
            'localised_name',
            'max_energy_usage',
            'inserter_extension_speed',
            'inserter_rotation_speed',
            'friendly_map_color',
            'enemy_map_color',
            'energy_source',
            'pollution',
            'belt_speed',
        ]
        missing_keys = []
        for i in fields.keys():
            if i not in assumed_keys:
                missing_keys.append(i)
        if missing_keys:
            raise ValueError(f"Keys not found in assumed_keys: {missing_keys}")
        return fields

    def json_out(self):
        content = super().json_out()
        content['max_energy_usage'] = self.max_energy_usage
        content['inserter_extension_speed'] = self.inserter_extension_speed
        content['inserter_rotation_speed'] = self.inserter_rotation_speed
        content['friendly_map_color'] = self.friendly_map_color
        content['enemy_map_color'] = self.enemy_map_color
        content['energy_source'] = self.energy_source.json_out()
        content['pollution'] = self.pollution
        content['belt_speed'] = self.belt_speed
        return content


class MineableProducts(BaseModel):
    type: str
    name: str
    probability: int
    amount: int

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        assumed_keys = [
            'type',
            'name',
            'probability',
            'amount',
        ]
        missing_keys = []
        for i in fields.keys():
            if i not in assumed_keys:
                missing_keys.append(i)
        if missing_keys:
            raise ValueError(f"Keys not found in assumed_keys: {missing_keys}")
        return fields

    def json_out(self):
        content = {
            'type': self.type,
            'name': self.name,
            'probability': self.probability,
            'amount': self.amount,
        }
        return content


class MineableProperties(BaseModel):
    minable: bool
    mining_time: float
    products: List[MineableProducts]
    mining_particle: str | None = None
    fluid_amount: int | None = None
    required_fluid: str | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        assumed_keys = [
            'minable',
            'mining_time',
            'products',
            'mining_particle',
            'fluid_amount',
            'required_fluid',
        ]
        missing_keys = []
        for i in fields.keys():
            if i not in assumed_keys:
                missing_keys.append(i)
        if missing_keys:
            raise ValueError(f"Keys not found in assumed_keys: {missing_keys}")
        return fields

    # @property
    # def process_time_seconds(self):
    #     if any([p for p in self.products if p.probability != 1]):
    #         print('FOUND A NON 1 PROBABILITY ITEM IN MINEABLE PRODUCTS')
    #         exit()
        
    #     return self.mining_time

    def json_out(self):
        content = {
            'minable': self.minable,
            'mining_time': self.mining_time,
            'products': [p.json_out() for p in self.products],
            'mining_particle': self.mining_particle,
            'fluid_amount': self.fluid_amount,
            'required_fluid': self.required_fluid,
        }
        return content


class FactorioDataResource(FactorioDataItemBase):
    resource_category: str
    mineable_properties: MineableProperties
    autoplace_specification: Dict | None = None
    energy_source: Dict

    process_uid: str | None = None
    consume_uids: Dict[str, float] = {}
    produce_uids: Dict[str, float] = {}
    machine_uid: str | None = None
    """
    Files:
        resource.json
    """

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        assumed_keys = [
            'project_uid',
            'filename',
            'name',
            'localised_name',
            'resource_category',
            'mineable_properties',
            'autoplace_specification',
            'energy_source',
        ]
        missing_keys = []
        for i in fields.keys():
            if i not in assumed_keys:
                missing_keys.append(i)
        if missing_keys:
            raise ValueError(f"Keys not found in assumed_keys: {missing_keys}")
        fields['autoplace_specification'] = None  # I dont think we want to track this today
        return fields

    def json_out(self):
        content = super().json_out()
        content['resource_category'] = self.resource_category
        content['mineable_properties'] = self.mineable_properties.json_out()
        content['autoplace_specification'] = self.autoplace_specification
        content['energy_source'] = self.energy_source
        content['process_uid'] = self.process_uid
        content['consume_uids'] = self.consume_uids
        content['produce_uids'] = self.produce_uids
        content['machine_uid'] = self.machine_uid
        return content

    def return_process(self):
        content = super().return_base_record()
        # content['name'] = self.name
        # content['project_uid'] = self.project_uid
        content['process_uid'] = self.process_uid
        content['consume_uids'] = self.consume_uids
        content['produce_uids'] = self.produce_uids
        content['machine_uid'] = self.machine_uid
        # content['process_time_seconds'] = self.mineable_properties.mining_time
        return content


class Ingredient(BaseModel):
    type: str
    name: str
    probability: float | None = None
    amount: float | None = None
    catalyst_amount: int | None = None
    amount_min: int | None = None
    amount_max: int | None = None
    fluidbox_index: int | None = None
    temperature: int | None = None
    minimum_temperature: float | None = None
    maximum_temperature: float | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        assumed_keys = [
            'project_uid',
            'type',
            'name',
            'probability',
            'amount',
            'catalyst_amount',
            'amount_min',
            'amount_max',
            'fluidbox_index',
            'temperature',
            'minimum_temperature',
            'maximum_temperature',
        ]
        missing_keys = []
        for i in fields.keys():
            if i not in assumed_keys:
                missing_keys.append(i)
        if missing_keys:
            raise ValueError(f"Keys not found in assumed_keys: {missing_keys}")
        return fields

    def json_out(self):
        content = {
            'type': self.type,
            'name': self.name,
            'probability': self.probability,
            'amount': self.amount,
            'catalyst_amount': self.catalyst_amount,
            'amount_min': self.amount_min,
            'amount_max': self.amount_max,
            'fluidbox_index': self.fluidbox_index,
            'temperature': self.temperature,
            'minimum_temperature': self.minimum_temperature,
            'maximum_temperature': self.maximum_temperature,
        }
        return content


class FactorioDataRecipe(FactorioDataItemBase):
    category: str
    order: str
    group: Dict
    subgroup: Dict
    enabled: bool
    hidden: bool
    hidden_from_player_crafting: bool
    emissions_multiplier: float
    energy: float
    ingredients: List[Ingredient] | None = None
    products: List[Ingredient]
    main_product: Ingredient | None = None

    process_uid: str | None = None
    consume_uids: Dict[str, float] = {}
    produce_uids: Dict[str, float] = {}
    machine_uid: str | None = None
    process_time_seconds: float | None = None
    """
    Files:
        recipe.json
    """

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        assumed_keys = [
            'project_uid',
            'filename',
            'name',
            'localised_name',
            'category',
            'order',
            'group',
            'subgroup',
            'enabled',
            'hidden',
            'hidden_from_player_crafting',
            'emissions_multiplier',
            'energy',
            'ingredients',
            'products',
            'main_product',
        ]
        if not fields['ingredients']:
            fields['ingredients'] = None

        missing_keys = []
        for i in fields.keys():
            if i not in assumed_keys:
                missing_keys.append(i)
        if missing_keys:
            raise ValueError(f"Keys not found in assumed_keys: {missing_keys}")
        return fields

    def json_out(self):
        if isinstance(self.ingredients, list):
            ingredients = [i.json_out() for i in self.ingredients]
        elif self.ingredients is None:
            ingredients = None
        else:
            ingredients = self.ingredients.json_out()

        if self.main_product:
            main_product = self.main_product.json_out()
        else:
            main_product = None

        content = super().json_out()
        content['category'] = self.category
        content['order'] = self.order
        content['group'] = self.group
        content['subgroup'] = self.subgroup
        content['enabled'] = self.enabled
        content['hidden'] = self.hidden
        content['hidden_from_player_crafting'] = self.hidden_from_player_crafting
        content['emissions_multiplier'] = self.emissions_multiplier
        content['energy'] = self.energy
        content['ingredients'] = ingredients
        content['products'] = [p.json_out() for p in self.products]
        content['main_product'] = main_product
        content['process_uid'] = self.process_uid
        content['consume_uids'] = self.consume_uids
        content['produce_uids'] = self.produce_uids
        content['machine_uid'] = self.machine_uid
        return content

    def return_process(self):
        content = super().return_base_record()
        content['project_uid'] = self.project_uid
        content['consume_uids'] = self.consume_uids
        content['produce_uids'] = self.produce_uids
        content['machine_uid'] = self.machine_uid
        content['process_time_seconds'] = self.process_time_seconds
        return content

# machines
# equipment
# fluids
# items
# weapons
# process
# resource
# power
# logistics


# 'active_mods.json'
# 'assembling-machine.json'
# 'boiler.json'
'equipment-grid.json'
'equipment.json'
# 'fluid.json'
# 'furnace.json'
# 'generator.json'
# 'inserter.json'
# 'item.json'
# 'lab.json'
# 'mining-drill.json'
'projectile.json'
# 'reactor.json'
# 'recipe.json'
# 'resource.json'
# 'rocket-silo.json'
# 'solar-panel.json'
'technology.json'
# 'transport-belt.json'



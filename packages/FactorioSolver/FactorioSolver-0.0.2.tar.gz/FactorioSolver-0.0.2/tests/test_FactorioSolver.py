from FactorioSolver import FactorioSolver
import pandas as pd

def test_contruction():
   model = FactorioSolver.Model("data/recipes.csv", "data/default_choice_map.json")
   assert len(model.get_data_graph().vs) > 0
   assert len(model.get_data_graph().es) > 0
   assert len(model.get_products()) > 0
   assert len(model.get_recipes()) > 0

def test_get_choice_map():
   model = FactorioSolver.Model("data/recipes.csv", "data/default_choice_map.json")
   choice_map = model.get_choice_map()
   assert not False in choice_map.apply(lambda x : x["Choice"] in x["Possibilities"], axis=1)
   
def test_get_product_usage_graph():
   model = FactorioSolver.Model("data/recipes.csv", "data/default_choice_map.json")
   graph = model.get_product_usage_graph("motor")
   assert(len(graph.vs) > 0)
   assert(len(graph.es) > 0)

def test_get_products_info():
   model = FactorioSolver.Model("data/recipes.csv", "data/default_choice_map.json")
   info = model.get_products_info("belt")
   assert len(info) > 0

def test_get_choice_list():
   model = FactorioSolver.Model("data/recipes.csv", "data/default_choice_map.json")
   choice_list = model.get_choice_list()
   assert type(choice_list) == list
   assert len(choice_list) > 0

   # no choice to build wood
   choice_list = model.get_choice_list("wood")
   assert len(choice_list) == 0

   # however se-rocket-science-pack should
   choice_list = model.get_choice_list("se-rocket-science-pack")
   assert len(choice_list) > 0
   
   # default choices should cover all of them though
   choice_list = model.get_choice_list("se-rocket-science-pack", model.get_choice_map())
   assert len(choice_list) == 0

def test_get_choice_list_choice_map():
   model = FactorioSolver.Model("data/recipes.csv", "data/default_choice_map.json")
   choice_list = model.get_choice_list()
   assert type(choice_list) == list
   assert len(choice_list) > 0

def test_print_product_usage():
   model = FactorioSolver.Model("data/recipes.csv", "data/default_choice_map.json")
   model.print_product_usage("motor", show_fig=False)

def test_compute_prod_graph():
   model = FactorioSolver.Model("data/recipes.csv", "data/default_choice_map.json")
   graph = model.compute_prod_graph({ "transport-belt" : 2, "se-rocket-science-pack":2 })
   assert len(graph.vs) > 0
   assert len(graph.es) > 0

def test_print_production_single():
   model = FactorioSolver.Model("data/recipes.csv", "data/default_choice_map.json")
   model.print_production_single("transport-belt", 2, show_fig=False)

def test_print_production():
   model = FactorioSolver.Model("data/recipes.csv", "data/default_choice_map.json")
   model.print_production({ "transport-belt" : 2, "se-rocket-science-pack":2 }, show_fig=False)


def test_set_choice_map():
   model = FactorioSolver.Model("data/recipes.csv", "data/default_choice_map.json")
   map = pd.read_json("data/default_choice_map.json")
   graph = model.compute_prod_graph({"advanced-circuit": 1})

   # default recipe is "electronic-circuit-stone" and uses stone-tablet
   assert len(graph.vs.select(name_eq="stone-tablet")) == 1
   assert len(graph.vs.select(name_eq="wood")) == 0
   datamap = model.get_choice_map()
   choice = datamap[datamap["Choice"] == "electronic-circuit-stone"]
   assert len(choice) == 1
   assert "electronic-circuit-stone" in choice.iloc[0]["Possibilities"]
   
   # make sure no ref is kept, the graph res should not have changed
   graph = model.compute_prod_graph({"advanced-circuit": 1})
   assert len(graph.vs.select(name_eq="stone-tablet")) == 1
   assert len(graph.vs.select(name_eq="wood")) == 0

   # change it to "electronic-circuit", which uses wood
   datamap.loc[choice.index, "Choice"] = "electronic-circuit"
   model.set_choice_map(datamap)
   graph = model.compute_prod_graph({"advanced-circuit": 1})
   assert len(graph.vs.select(name_eq="stone-tablet")) == 0
   assert len(graph.vs.select(name_eq="wood")) == 1

if __name__ == "__main__":
   print(__name__, type(__name__)) 
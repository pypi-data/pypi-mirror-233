
#include "include/NodeCT.hpp"
#include "include/ComponentTree.hpp"
#include "include/AttributeComputedIncrementally.hpp"
#include "include/AttributeFilters.hpp"
#include "include/AdjacencyRelation.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include <iterator>
#include <utility>


namespace py = pybind11;


void init_NodeCT(py::module &m){
    py::class_<NodeCT>(m, "NodeCT")
		.def(py::init<>())
		.def_property_readonly("id", &NodeCT::getIndex )
        .def_property_readonly("rep", &NodeCT::getRep )
		.def_property_readonly("cnps", &NodeCT::getCNPs )
		.def_property_readonly("level", &NodeCT::getLevel )
		.def_property_readonly("children", &NodeCT::getChildren )
		.def_property_readonly("parent", &NodeCT::getParent )
        .def_property_readonly("areaCC", &NodeCT::getAreaCC )
        .def_property_readonly("numDescendants", &NodeCT::getNumDescendants )
        .def_property_readonly("numSiblings", &NodeCT::getNumSiblings )
        .def("pixelsOfCC",&NodeCT::getPixelsOfCC )
        .def("nodesOfPathToRoot",&NodeCT::getNodesOfPathToRoot )
        .def("nodesDescendants",&NodeCT::getNodesDescendants );
        
    py::class_<NodeCT::IteratorPixelsOfCC>(m, "IteratorPixelsOfCC")
		.def(py::init<NodeCT *, int>())
		.def_property_readonly("begin", &NodeCT::IteratorPixelsOfCC::begin )
        .def_property_readonly("end", &NodeCT::IteratorPixelsOfCC::end )
        .def("__iter__", [](NodeCT::IteratorPixelsOfCC &iter) {
            return py::make_iterator(iter.begin(), iter.end());
            }, py::keep_alive<0, 1>()); /* Keep vector alive while iterator is used */

    py::class_<NodeCT::IteratorNodesOfPathToRoot>(m, "IteratorNodesOfPathToRoot")
		.def(py::init<NodeCT *>())
		.def_property_readonly("begin", &NodeCT::IteratorNodesOfPathToRoot::begin )
        .def_property_readonly("end", &NodeCT::IteratorNodesOfPathToRoot::end )
        .def("__iter__", [](NodeCT::IteratorNodesOfPathToRoot &iter) {
            return py::make_iterator(iter.begin(), iter.end());
            }, py::keep_alive<0, 1>()); /* Keep vector alive while iterator is used */
            
    py::class_<NodeCT::IteratorNodesDescendants>(m, "IteratorNodesDescendants")
		.def(py::init<NodeCT *, int>())
		.def_property_readonly("begin", &NodeCT::IteratorNodesDescendants::begin )
        .def_property_readonly("end", &NodeCT::IteratorNodesDescendants::end )
        .def("__iter__", [](NodeCT::IteratorNodesDescendants &iter) {
            return py::make_iterator(iter.begin(), iter.end());
            }, py::keep_alive<0, 1>()); /* Keep vector alive while iterator is used */
}



void init_ComponentTree(py::module &m){
      py::class_<ComponentTree>(m, "ComponentTree")
        .def(py::init<py::array_t<int> &, int, int, bool, double>())
        .def(py::init<py::array_t<int> &, int, int, bool>())
        .def("reconstructionImage", &ComponentTree::reconstructionImage )
		.def_property_readonly("numNodes", &ComponentTree::getNumNodes )
        .def_property_readonly("listNodes", &ComponentTree::getListNodes )
        .def_property_readonly("root", &ComponentTree::getRoot )
        .def_static("computerParent", &ComponentTree::computerParent)
		.def_property_readonly("parent", &ComponentTree::getParent )
        .def_property_readonly("orderedPixels", &ComponentTree::getOrderedPixels );
        
        
        //.def("prunningMin", py::overload_cast<py::array_t<double> &, double>(&ComponentTree::prunningMin))
        //.def("prunningMin", &ComponentTree::prunningMin)
        //.def("computerArea", &ComponentTree::computerArea)
        //.def("prunningMin", py::overload_cast<py::array_t<double> &, double>(&ComponentTree::prunningMin))
}


void init_AttributeComputedIncrementally(py::module &m){
    	py::class_<AttributeComputedIncrementally>(m, "Attribute")
        //.def_static("computerAttribute", &AttributeComputedIncrementally::computerAttribute)
        .def_static("computerBasicAttributes", &AttributeComputedIncrementally::computerBasicAttributes)
        .def_static("computerArea", &AttributeComputedIncrementally::computerArea);
}

void init_AttributeFilters(py::module &m){
    py::class_<AttributeFilters>(m, "AttributeFilters")
    .def(py::init<ComponentTree *>())
    .def("filteringMin", py::overload_cast<py::array_t<double> &, double>(&AttributeFilters::filteringByPruningMin))
    .def("filteringMin", py::overload_cast<std::vector<bool>>(&AttributeFilters::filteringByPruningMin))
    .def("filteringMax", py::overload_cast<std::vector<bool>>(&AttributeFilters::filteringByPruningMax))
    .def("filteringDirectRule", py::overload_cast<std::vector<bool>>(&AttributeFilters::filteringByDirectRule))
    .def("filteringSubtractiveRule", py::overload_cast<std::vector<bool>>(&AttributeFilters::filteringBySubtractiveRule))
    .def("filteringSubtractiveScoreRule", py::overload_cast<std::vector<double>>(&AttributeFilters::filteringBySubtractiveScoreRule))
    .def("filteringMax", py::overload_cast<py::array_t<double> &, double>(&AttributeFilters::filteringByPruningMax));
}


void init_AdjacencyRelation(py::module &m){
    	py::class_<AdjacencyRelation>(m, "AdjacencyRelation")
        .def(py::init<int, int, double>())
        .def_property_readonly("size", &AdjacencyRelation::getSize )
        .def("getAdjPixels", py::overload_cast<int, int>( &AdjacencyRelation::getAdjPixels ));

}

PYBIND11_MODULE(ctreelearn, m) {
    // Optional docstring
    m.doc() = "A simple library for learning of connected filters based on component trees";
    
    init_NodeCT(m);
    init_ComponentTree(m);
    init_AttributeComputedIncrementally(m);
    init_AttributeFilters(m);
    init_AdjacencyRelation(m);
}

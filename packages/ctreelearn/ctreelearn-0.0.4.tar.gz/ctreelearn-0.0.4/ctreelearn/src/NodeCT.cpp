#include "../include/NodeCT.hpp"
#include "../include/AdjacencyRelation.hpp"

#include <list>

NodeCT::NodeCT(){}

NodeCT::NodeCT(int index, int rep, NodeCT* parent, int level) {
		this->index = index;
        this->rep = rep;
        this->parent = parent;
        this->level = level;
}

void NodeCT::addCNPs(int p) {
    this->cnps.push_back(p);
}

void NodeCT::addChild(NodeCT* child) {
	this->children.push_back(child);
}

int NodeCT::getRep(){ return this->rep; }

int NodeCT::getIndex(){ return this->index; }

int NodeCT::getLevel(){ return this->level; }

int NodeCT::getAreaCC() { return this->areaCC; }

void NodeCT::setAreaCC(int area) { this->areaCC = area; }

int NodeCT::getNumDescendants() { return this->numDescendants; }

void NodeCT::setNumDescendants(int num) { this->numDescendants = num; }

NodeCT* NodeCT::getParent(){  return this->parent; }

std::list<int> NodeCT::getCNPs(){  return this->cnps; }

std::list<NodeCT*> NodeCT::getChildren(){  return this->children; }

int NodeCT::getNumSiblings() {
    if(this->parent != nullptr)
		return this->parent->getChildren().size();
	else
		return 0;
}

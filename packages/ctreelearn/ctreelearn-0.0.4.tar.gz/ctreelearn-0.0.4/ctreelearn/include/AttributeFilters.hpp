
#include "../include/NodeCT.hpp"
#include "../include/ComponentTree.hpp"
#include "../include/AttributeComputedIncrementally.hpp"

#include <stack>
#include <vector>
#include <limits.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#ifndef ATTRIBUTE_FILTERS_H
#define ATTRIBUTE_FILTERS_H

#define UNDEF -999999999999

class AttributeFilters{
    private:
        ComponentTree *tree;

    public:

    AttributeFilters(ComponentTree *tree);

    py::array_t<int> filteringByPruningMin(py::array_t<double> &attr, double threshold);

    py::array_t<int> filteringByPruningMax(py::array_t<double> &attr, double threshold);

    py::array_t<int> filteringByPruningMin(std::vector<bool> criterion);

    py::array_t<int> filteringByPruningMax(std::vector<bool> criterion);

    py::array_t<int> filteringByDirectRule(std::vector<bool> criterion);

    py::array_t<int> filteringBySubtractiveRule(std::vector<bool> criterion);

    py::array_t<float> filteringBySubtractiveScoreRule(std::vector<double> criterion);

    static void filteringBySubtractiveScoreRule(ComponentTree *tree, std::vector<double> prob, float *imgOutput){
        float mapLevel[tree->getNumNodes()];
        
        //the root is always kept
        mapLevel[0] = tree->getRoot()->getLevel();

        for(NodeCT* node: tree->getListNodes()){
            if(node->getParent() != nullptr){ 
                int h = std::abs(node->getLevel() - node->getParent()->getLevel());
                mapLevel[node->getIndex()] = (float) mapLevel[node->getParent()->getIndex()] + (h * prob[node->getIndex()]);
            }

        }
        for(NodeCT* node: tree->getListNodes()){
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = mapLevel[node->getIndex()];
            }
        }
    }


    static void filteringBySubtractiveRule(ComponentTree *tree, std::vector<bool> criterion, int *imgOutput){
        int mapLevel[tree->getNumNodes()];
        
        //the root is always kept
        mapLevel[0] = tree->getRoot()->getLevel();

        for(NodeCT* node: tree->getListNodes()){
            if(node->getParent() != nullptr){ 
                if(criterion[node->getIndex()]){
                    int h = std::abs(node->getLevel() - node->getParent()->getLevel());
                    mapLevel[node->getIndex()] = mapLevel[node->getParent()->getIndex()] + h;
                }
                else
                    mapLevel[node->getIndex()] = mapLevel[node->getParent()->getIndex()];
            }

        }
        for(NodeCT* node: tree->getListNodes()){
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = mapLevel[node->getIndex()];
            }
        }
    }

    static void filteringByDirectRule(ComponentTree *tree, std::vector<bool> criterion, int *imgOutput){
        int mapLevel[tree->getNumNodes()];

        //the root is always kept
        mapLevel[0] = tree->getRoot()->getLevel();

        for(NodeCT* node: tree->getListNodes()){
            if(node->getParent() != nullptr){ 
                if(criterion[node->getIndex()])
                    mapLevel[node->getIndex()] = node->getLevel();
                else
                    mapLevel[node->getIndex()] = mapLevel[node->getParent()->getIndex()];
            }

        }
        for(NodeCT* node: tree->getListNodes()){
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = mapLevel[node->getIndex()];
            }
        }
        /*std::stack<NodeCT*> s;
        s.push(tree->getRoot());
        std::stack<int> sLevel;
        sLevel.push(tree->getRoot()->getLevel());
        criterion[0] = true; //the root is always kept
        
        while(!s.empty()){
            NodeCT *node = s.top(); s.pop();
            int level = sLevel.top(); sLevel.pop();
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = level;
            }

            for (NodeCT *child: node->getChildren()){
                s.push(child);
                if(criterion[child->getIndex()]){
                    sLevel.push(child->getLevel());
                }else{
                    sLevel.push(level);
                }
            }
        }*/
    }

    static void filteringByPruningMin(ComponentTree *tree, std::vector<bool> criterion, int *imgOutput){
        std::stack<NodeCT*> s;
        s.push(tree->getRoot());
        while(!s.empty()){
            NodeCT *node = s.top(); s.pop();
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = node->getLevel();;
            }
            for (NodeCT *child: node->getChildren()){
                if(criterion[child->getIndex()]){
                    s.push(child);
                }else{
                    for(int pixel: child->getPixelsOfCC()){
                        imgOutput[pixel] = child->getLevel();
                    }
                }
            }
        }
    }

    static void filteringByPruningMax(ComponentTree *tree, std::vector<bool> _criterion, int *imgOutput){
        
        bool criterion[tree->getNumNodes()];
        AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
            [&criterion, _criterion](NodeCT* node) -> void { //pre-processing
                if(!_criterion[node->getIndex()])
                    criterion[node->getIndex()] = true;
                else
                    criterion[node->getIndex()] = false;
            },
            [&criterion](NodeCT* parent, NodeCT* child) -> void { 
                criterion[parent->getIndex()] = (criterion[parent->getIndex()] & criterion[child->getIndex()]);
            },
            [](NodeCT* node) -> void { //post-processing
                                        
            }
        );

        std::stack<NodeCT*> s;
        s.push(tree->getRoot());
        while(!s.empty()){
            NodeCT *node = s.top(); s.pop();
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = node->getLevel();
            }
            for (NodeCT *child: node->getChildren()){
                if(!criterion[child->getIndex()]){
                    s.push(child);
                }else{
                    for(int pixel: child->getPixelsOfCC()){
                        imgOutput[pixel] = child->getLevel();
                    }
                }
            }
        }
    }


    static void filteringByPruningMin(ComponentTree *tree, double *attribute, double threshold, int *imgOutput){
        std::stack<NodeCT*> s;
        s.push(tree->getRoot());
        while(!s.empty()){
            NodeCT *node = s.top(); s.pop();
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = node->getLevel();
            }
            for (NodeCT *child: node->getChildren()){
                if(attribute[child->getIndex()] > threshold){
                    s.push(child);
                }else{
                    for(int pixel: child->getPixelsOfCC()){
                        imgOutput[pixel] = child->getLevel();
                    }
                }
                
            }
        }
    }

    static void filteringByPruningMax(ComponentTree *tree, double *attribute, double threshold, int *imgOutput){
        
        bool criterion[tree->getNumNodes()];
        AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
            [&criterion, attribute, threshold](NodeCT* node) -> void { //pre-processing
                if(attribute[node->getIndex()] <= threshold)
                    criterion[node->getIndex()] = true;
                else
                    criterion[node->getIndex()] = false;
            },
            [&criterion, attribute, threshold](NodeCT* parent, NodeCT* child) -> void { 
                criterion[parent->getIndex()] = (criterion[parent->getIndex()] & criterion[child->getIndex()]);
            },
            [&criterion, attribute, threshold](NodeCT* node) -> void { //post-processing
                                        
            }
        );

        std::stack<NodeCT*> s;
        s.push(tree->getRoot());
        while(!s.empty()){
            NodeCT *node = s.top(); s.pop();
            for (int pixel : node->getCNPs()){
                imgOutput[pixel] = node->getLevel();
            }
            for (NodeCT *child: node->getChildren()){
                if(!criterion[child->getIndex()]){
                    s.push(child);
                }else{
                    for(int pixel: child->getPixelsOfCC()){
                        imgOutput[pixel] = child->getLevel();
                    }
                }
            }
        }
    }
};


#endif
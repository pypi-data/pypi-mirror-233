#include "../include/NodeCT.hpp"
#include "../include/ComponentTree.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <algorithm> 
#include <cmath>
#include <iostream>


#ifndef ATTRIBUTE_COMPUTED_INCREMENTALLY_H
#define ATTRIBUTE_COMPUTED_INCREMENTALLY_H

#define PI 3.14159265358979323846

class AttributeComputedIncrementally{

public:
    virtual void preProcessing(NodeCT *v);

    virtual void mergeChildren(NodeCT *parent, NodeCT *child);

    virtual void postProcessing(NodeCT *parent);

    void computerAttribute(NodeCT *root);

	static void computerAttribute(NodeCT* root, 
										std::function<void(NodeCT*)> preProcessing,
										std::function<void(NodeCT*, NodeCT*)> mergeChildren,
										std::function<void(NodeCT*)> postProcessing ){
		
		preProcessing(root);
			
		for(NodeCT *child: root->getChildren()){
			AttributeComputedIncrementally::computerAttribute(child, preProcessing, mergeChildren, postProcessing);
			mergeChildren(root, child);
		}

		postProcessing(root);
	}

	static py::array_t<float> computerArea(ComponentTree *tree){
		const int n = tree->getNumNodes();
		float *attrs = new float[n];
		AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
			[&attrs](NodeCT* node) -> void { //pre-processing
				attrs[node->getIndex()] = node->getCNPs().size(); //area
			},
			[&attrs](NodeCT* parent, NodeCT* child) -> void { //merge-processing
				attrs[parent->getIndex()] += attrs[child->getIndex()];
			},
			[](NodeCT* node) -> void { //post-processing			
		});
	    py::array_t<float> numpy = py::array(py::buffer_info(
			attrs,            
			sizeof(float),     
			py::format_descriptor<float>::value, 
			1,         
			{  n }, 
			{ sizeof(float) }
	    ));
		return numpy;
	}

    static py::list computerBasicAttributes(ComponentTree *tree){
	    const int numAttribute = 19;
		const int n = tree->getNumNodes();
		float *attrs = new float[n * numAttribute];
		/*
		0 - area
		1 - volume
		2 - level
		3 - mean level
		4 - variance level
		5 - Box width
		6 - Box height
		7 - rectangularity
		8 - ratio (Box width, Box height)
		9 - moment20
		10 - moment02
		11 - moment11
		12 - inertia
		13 - orientation
		14 - lenght major axis
		15 - lenght minor axis
		16 - eccentricity = alongation
		17 - compactness = circularity
		*/
		
		int xmax[n]; //min value
		int ymax[n]; //min value
		int xmin[n]; //max value
		int ymin[n]; //max value
		long int m10[n];
		long int m01[n];
		long int m20[n];
		long int m02[n];
		long int m11[n];
		long double graySquare[n];

		int numCols = tree->getNumColsOfImage();
		int numRows = tree->getNumRowsOfImage();
		

	    AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
						[&attrs, n,  &xmax, &ymax, &xmin, &ymin, &m10, &m01,&m11, &m20, &m02, &graySquare, numCols, numRows](NodeCT* node) -> void {
							attrs[node->getIndex()         ] = node->getCNPs().size(); //area
							attrs[node->getIndex() + n     ] = node->getCNPs().size() * node->getLevel(); //volume
							attrs[node->getIndex() + (n*2) ] = node->getLevel(); //level

							xmax[node->getIndex()] = 0;
							ymax[node->getIndex()] = 0;
							xmin[node->getIndex()] = numCols;
							ymin[node->getIndex()] = numRows;
							m10[node->getIndex()] = 0;
							m11[node->getIndex()] = 0;
							m01[node->getIndex()] = 0;
							m20[node->getIndex()] = 0;
							m02[node->getIndex()] = 0;
							graySquare[node->getIndex()] = std::pow(node->getLevel(), 2) * node->getCNPs().size(); //computando: f(x)^2	
							for(int p: node->getCNPs()) {
								int x = p % numCols;
								int y = p / numCols;
								xmin[node->getIndex()] = std::min(xmin[node->getIndex()], x);
								ymin[node->getIndex()] = std::min(ymin[node->getIndex()], y);
								xmax[node->getIndex()] = std::max(xmax[node->getIndex()], x);
								ymax[node->getIndex()] = std::max(ymax[node->getIndex()], y);
								m10[node->getIndex()] += x;
								m01[node->getIndex()] += y;
								m11[node->getIndex()] += x*y;
								m20[node->getIndex()] += x*x;
								m02[node->getIndex()] += y*y;
								
							}
							


						},
						[&attrs, n, &xmax, &ymax, &xmin, &ymin, &m10, &m01,&m11, &m20, &m02, &graySquare](NodeCT* parent, NodeCT* child) -> void {
							attrs[parent->getIndex()       ] += attrs[child->getIndex()]; //area
							attrs[parent->getIndex() + n   ] += attrs[child->getIndex() + n]; //volume
							
							graySquare[parent->getIndex()] += graySquare[child->getIndex()]; //variancia

							ymax[parent->getIndex()] = std::max(ymax[parent->getIndex()], ymax[child->getIndex()]);
							xmax[parent->getIndex()] = std::max(xmax[parent->getIndex()], xmax[child->getIndex()]);
							
							ymin[parent->getIndex()] = std::min(ymin[parent->getIndex()], ymin[child->getIndex()]);
							xmin[parent->getIndex()] = std::min(xmin[parent->getIndex()], xmin[child->getIndex()]);
		
							m10[parent->getIndex()] += m10[child->getIndex()];
							m01[parent->getIndex()] += m01[child->getIndex()];
							m11[parent->getIndex()] += m11[child->getIndex()];
							m20[parent->getIndex()] += m20[child->getIndex()];
							m02[parent->getIndex()] += m02[child->getIndex()];

						},
						[&attrs, n, &xmax, &ymax, &xmin, &ymin, &m10, &m01, &m11, &m20, &m02, &graySquare](NodeCT* node) -> void {
							
							float area = attrs[node->getIndex()];
							float volume = attrs[node->getIndex() + n];
							float width = xmax[node->getIndex()] - xmin[node->getIndex()] + 1;	
							float height = ymax[node->getIndex()] - ymin[node->getIndex()] + 1;	
							
							attrs[node->getIndex() + (n*3) ] = volume / area; //mean level
							attrs[node->getIndex() + (n*4) ] = (graySquare[node->getIndex()] / area) - std::pow((volume / area),2); //variance: E(f(x)^2) - E(f(x))^2
							attrs[node->getIndex() + (n*18) ] = std::sqrt(attrs[node->getIndex() + (n*4) ]); //desvio padrao
							attrs[node->getIndex() + (n*5) ] = width;
							attrs[node->getIndex() + (n*6) ] = height;
							
							attrs[node->getIndex() + (n*7) ] = area / (width * height);
							attrs[node->getIndex() + (n*8) ] = std::max(width, height) / std::min(width, height);
							

							/********************************
							       Momentos centrais
							*********************************/
							float xCentroid = m10[node->getIndex()] / attrs[node->getIndex()];
							float yCentroid = m01[node->getIndex()] / attrs[node->getIndex()];	
							
							attrs[node->getIndex() + (n*9) ] = m20[node->getIndex()] - (m10[node->getIndex()] * xCentroid);
							attrs[node->getIndex() + (n*10) ]= m02[node->getIndex()] - (m01[node->getIndex()] * yCentroid);
							attrs[node->getIndex() + (n*11) ] = m11[node->getIndex()] - (xCentroid * m01[node->getIndex()]); //(m10[node->getIndex()] - xCentroid) * (m01[node->getIndex()] - yCentroid);

							float moment20 = attrs[node->getIndex()+(n*9)];
							float moment02 = attrs[node->getIndex()+(n*10)];
							float moment11 = attrs[node->getIndex()+(n*11)];
							
							if(area > 1){
								auto normMoment = [area](float moment, int p, int q){ return moment / std::pow( area, (p + q + 2.0) / 2.0); };
								float a1 = moment20 + moment02 + std::sqrt( std::pow(moment20 - moment02, 2) + 4 * std::pow(moment11, 2));
								float a2 = moment20 + moment02 - std::sqrt( std::pow(moment20 - moment02, 2) + 4 * std::pow(moment11, 2));
								attrs[node->getIndex() + (n*12) ] = normMoment(moment02, 0, 2) + normMoment(moment20, 2, 0); //hu = inertia
								attrs[node->getIndex() + (n*13) ] = 0.5 * std::atan2(2 * moment11, moment20 - moment02); //orientation
								
								attrs[node->getIndex() + (n*14) ] = std::sqrt( (2 * a1) / area ); //lenght major axis
								attrs[node->getIndex() + (n*15) ] = std::sqrt( (2 * a2) / area ); //lenght minor axis
								
								attrs[node->getIndex() + (n*16) ] = (a2 != 0? a1 / a2 : a1 / 0.1); //eccentricity
								
								attrs[node->getIndex() + (n*17) ] = ( 1.0 / (2*PI) ) *  ( area / (moment20 + moment02) ); //compactness 
							}	

		});

		

		py::dict dict;
        dict[py::str("AREA")] = 0;
		dict[py::str("VOLUME")] = 1;
		dict[py::str("LEVEL")] = 2;
		dict[py::str("MEAN_LEVEL")] = 3;
		dict[py::str("VARIANCE_LEVEL")] = 4;
		dict[py::str("WIDTH")] = 5;
		dict[py::str("HEIGHT")] = 6;
		dict[py::str("RETANGULARITY")] = 7;
		dict[py::str("RATIO_WH")] = 8;
		dict[py::str("MOMENT_02")] = 9;
		dict[py::str("MOMENT_20")] = 10;
		dict[py::str("MOMENT_11")] = 11;
		dict[py::str("INERTIA")] = 12;
		dict[py::str("ORIENTATION")] = 13;
		dict[py::str("LEN_MAJOR_AXIS")] = 14;
		dict[py::str("LEN_MINOR_AXIS")] = 15;
		dict[py::str("ECCENTRICITY")] = 16;
		dict[py::str("COMPACTNESS")] = 17;
		dict[py::str("STD_LEVEL")] = 18;
		
		
		
	    py::array_t<float> numpy = py::array(py::buffer_info(
			attrs,            
			sizeof(float),     
			py::format_descriptor<float>::value, 
			2,         
			{  n,  numAttribute }, 
			{ sizeof(float), sizeof(float) * n }
	    ));
		

		py::list list;
		list.append(dict);
		list.append(numpy);
		return list;
    }



};

#endif 
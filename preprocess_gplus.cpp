#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>


int main () {
	std::string line;
  std::ifstream gplus_file ("gplus_combined.txt");

  std::ofstream gplus_mapped("gplus_combined_mapped.txt");

  std::vector<std::string> list;
  list.reserve(107614);


  if (gplus_file.is_open() && gplus_mapped.is_open()) {
    while ( getline (gplus_file,line) ) {
    	
    	std::size_t delimiter_position = line.find(' ');
    	std::string str1 = line.substr(0, delimiter_position);
    	std::string str2 = line.substr(delimiter_position+1);

      //std::cout << "String 1: "  << str1 << ". " << "String 2: " << str2 << '\n';
 			
    	
 			   	
    	std::cout << str1_map << " " << str2_map << std::endl;


      //list.push_back(2323)
    }
    gplus_file.close();
    gplus_mapped.close();
  }

  else std::cout << "Unable to open file"; 

  return 0;


}
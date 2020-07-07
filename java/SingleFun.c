#include <iostream>
#include <vector>

using namespace std;


int main() {
    vector<int> nums;
    for (int i = 0; i < 5000; i++) {
        nums.push_back(i);
    }
	for (int i = 0; i < 5000; i++) {
        for (int j = 0; j <nums.size() - 1; j++) {
            nums[j] = nums[j] % nums[j+1] + 1;
        }
    }
	return 0;
}
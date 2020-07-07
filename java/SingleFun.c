#include <iostream>
#include <vector>

using namespace std;


int main() {
    int times = 5;
    while(times > 0) {
        times--;
        vector<int> nums;
        for (int i = 0; i < 10000; i++) {
            nums.push_back(i);
        }
        for (int i = 0; i < 10000; i++) {
            for (int j = 0; j <nums.size() - 1; j++) {
                nums[j] = nums[j] % nums[j+1] + 1;
            }
        }
        cout << "Finish" << " " << (5 - times) << endl;
    }

	return 0;
}
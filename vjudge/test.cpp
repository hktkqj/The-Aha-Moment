#include<iostream>
using namespace std;

int main()
{
	int a,b,c;
	while (cin>>a>>b>>c) {
		if (a%2==0||b%2==0||c%2==0)
			cout<<"Yes"<<endl;
		else cout<<"No"<<endl;
	}
}

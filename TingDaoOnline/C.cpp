#include<iostream>
#include<cstdio>
#include<string>
#include<cstdlib>
#include<ctime>
using namespace std;
struct Command{
	int cmd; //cmd : 0-add, 1=equal, 2=uneq, 3=less, 4=great
	int opt1,opt2;	
	
}command[10010];

int main()
{
	auto a=1.12;
	int T; string s;
	cin>>T;
	while (T--) {
		int n;
		cin>>n;
		for (int i=1;i<=n;i++) {
			cin>>s;
			if (s=="add") {
				scanf("%d",&command[i].opt1);
				command[i].cmd=0;
			} else if (s=="beq") {
				scanf("%d %d",&command[i].opt1,&command[i].opt2);
				command[i].cmd=1;
			} else if (s=="bne") {
				scanf("%d %d",&command[i].opt1,&command[i].opt2);
				command[i].cmd=2;
			} else if (s=="blt") {
				scanf("%d %d",&command[i].opt1,&command[i].opt2);
				command[i].cmd=3;
			} else if (s=="bgt") {
				scanf("%d %d",&command[i].opt1,&command[i].opt2);
				command[i].cmd=4;
			}
		}
		int now=0,cnt=0,flag=0;
		srand(time(NULL));
		if (n>1000){ cout<<"No\n"; continue; }
		for (int i=1;i<=n;){
			cnt++;
			if (command[i].cmd==0) {
				now+=command[i].opt1;
				now%=256;
				++i;
			} else
			if (command[i].cmd==1) {
				if (now==command[i].opt1) {
					i=command[i].opt2;
				} else ++i;
			} else 
			if (command[i].cmd==2) {
				if (now!=command[i].opt1) {
					i=command[i].opt2;
				} else ++i;
			} else 
			if (command[i].cmd==3) {
				if (now<command[i].opt1) {
					i=command[i].opt2;
				} else ++i;
			} else {
				if (now>command[i].opt2) {
					i=command[i].opt2;
				} else ++i;
			}
			if (n<=1000&&cnt>(n*4000)) {
				printf("No\n");
				flag=1;
				break;
			} 
		}
		if (!flag) printf("Yes\n");
	}
}

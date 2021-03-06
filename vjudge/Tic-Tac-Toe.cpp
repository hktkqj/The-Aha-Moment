#include<iostream>
#include<cstdio>
#include<cstring>
#include<map>
#include<cmath>
#include<bits/stdc++.h>
using namespace std;
int state[4][4];
//Statement: First hand: 'o',shown as 1 in array; Second hand: 'x', shown as -1 in array;
//Clarify: There's no more than 3^9 state in Tic-Tac-Toe game, we used an array of [20000](int);
//Statement: 0 stands for not solved, 1 stands for first-hand win and -1 vice versa
//Sample: 123012321: 0 for not occupied, 1 for 'o' and 2 for 'x'
bool visit[20000];
int nextstep[11];

void unzip(int statenum) 
{
	for (int i=3;i>=1;i--)
		for (int j=3;j>=1;j--) {
			if (statenum%10==0)
				state[i][j]=0;
			else if (statenum%10==1)
				state[i][j]=1;
			else if (statenum%10==2)
				state[i][j]=-1;
			statenum/=10;
		}
}

int zip()
{
	int tempstate=0;
	for (int i=1;i<=3;i++)
		for (int j=1;j<=3;j++) {
			if (state[i][j]==1)
				tempstate+=1;
			else if (state[i][j]==-1) 
				tempstate+=2;
			tempstate*=10; 
		}
	return tempstate/10;
}

int rank() //No parameter as we used global array state[4][4]
{
	//Check line winner
	for (int i=1;i<=3;i++) {
		int sum=0;
		for (int j=1;j<=3;j++) 
			sum+=state[i][j];
		if (abs(sum)==3) {
			if (sum>0) 
				return 1; //Firsr win situation
			else if (sum<0) 
				return -1; //Second win situation
		}
	}
	//Check row winner
	for (int i=1;i<=3;i++) {
		int sum=0;
		for (int j=1;j<=3;j++) 
			sum+=state[j][i];
		if (abs(sum)==3) {
			if (sum>0) 
				return 1; 
			else if (sum<0) 
				return -1; //Same as before
		}
	}
	//Check right slope
	int sum=0;
	for (int i=1;i<=3;i++) 
		sum+=state[i][i];
	if (abs(sum)==3) {
		if (sum>0) 
			return 1; 
		else if (sum<0) 
			return -1; 
	}
	sum=0;
	for (int i=1;i<=3;i++) 
		sum+=state[i][4-i];
	if (abs(sum)==3) {
		if (sum>0) 
			return 1; 
		else if (sum<0) 
			return -1; 
	}
	//If not solved
	return 0;
}

int And_Or_Tree_Search(int nowstate,bool First,int depth) 
{
	//First == true : get max rank; First == false :get min rank
	unzip(nowstate);
	//printf("%d\n",nowstate);
	int staterank=rank()*(10-depth),nextopt;
	if (staterank)
		return staterank; 
	int nxtstate;
	if (First) {
		int maxx=-10;
		for (int i=1;i<=3;i++)
			for (int j=1;j<=3;j++) 
				if (state[i][j]==0) {
					state[i][j]=1;
					int temp=And_Or_Tree_Search(zip(),!First,depth+1)*(10-depth) ;
					if (temp>maxx) { maxx=temp; nxtstate=zip();	}
					state[i][j]=0;
				}
	} else {
		int minn=10;
		for (int i=1;i<=3;i++)
			for (int j=1;j<=3;j++) 
				if (state[i][j]==0) {
					state[i][j]=-1;
					int temp=And_Or_Tree_Search(zip(),!First,depth+1)*(10-depth) ;
					if (temp<minn) { minn=temp; nxtstate=zip();	}
					state[i][j]=0;
				}
	}
	nextstep[depth]=nxtstate;
}


int main()
{
	memset(state,0,sizeof(state));
	memset(visit,0,sizeof(visit));
	visit[0]=true;
	And_Or_Tree_Search(0,true,1);
	while (1) {
		unzip(nextstep[1]);
		for (int i=1;i<=3;i++) {
			for (int j=1;j<=3;j++)
				printf("%c ",state[i][j]==0?'.':(state[i][j]==1?'o':'x'));
			printf("\n");				
		}
		printf("Please select next move: ");
		int x,y; cin>>x>>y;
		state[x][y]=-1;
		And_Or_Tree_Search(zip(),true,1);
	}
}

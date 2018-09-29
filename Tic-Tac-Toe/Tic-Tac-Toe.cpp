#include<iostream>
#include<cstdio>
#include<cstring>
#include<map>
#include<cmath>
#include<bits/stdc++.h>
#include<map>
using namespace std;
int state[4][4];
//Statement: First hand: 'o',shown as 1 in array; Second hand: 'x', shown as -1 in array;
//Clarify: There's no more than 3^9 state in Tic-Tac-Toe game, we used an array of [20000](int);
//Statement: 0 stands for not solved, 1 stands for first-hand win and -1 vice versa
//Sample: 123012321: 0 for not occupied, 1 for 'o' and 2 for 'x'
map <int,int> save;
int nextstep;

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

bool checkdraw()
{
	if (rank()) return false;
	for (int i=1;i<=3;i++)
		for (int j=1;j<=3;j++)
			if (state[i][j]==0) return false;
	return true;
}

int And_Or_Tree_Search(int nowstate,bool First) 
{
	//First == true : get max rank; First == false :get min rank
	unzip(nowstate);
	//printf("%d\n",nowstate);
	int staterank=rank(),nextopt;
	if (staterank||checkdraw())
		return staterank; 
	int nxtstate;
	if (First) {
		int maxx=-10;
		for (int i=1;i<=3;i++)
			for (int j=1;j<=3;j++) 
				if (state[i][j]==0) {
					state[i][j]=1;
					int next1=zip();
					if (!save[next1]) {
						int temp=And_Or_Tree_Search(next1,!First) ;
						if (temp>maxx) { maxx=temp; nxtstate=next1; }
						save[next1]=temp;
					} else  {
						int temp=save[next1];
						if (temp>maxx) { maxx=temp; nxtstate=next1;	}						
					}
					state[i][j]=0;
				}
	} else {
		int minn=10;
		for (int i=1;i<=3;i++)
			for (int j=1;j<=3;j++) 
				if (state[i][j]==0) {
					state[i][j]=-1;
					int next1=zip();
					if (!save[next1]) {
						int temp=And_Or_Tree_Search(next1,!First);
						if (temp<minn) minn=temp;
						save[next1]=temp;
					} else {
						int temp=save[next1];
						if (temp<minn) minn=temp;
					}
					state[i][j]=0;
				}
		return minn==10?0:minn;
		//return minn;
	}
	nextstep=nxtstate;
}


int main()
{
	memset(state,0,sizeof(state));
	And_Or_Tree_Search(0,true);
	while (1) {
		unzip(nextstep);
		printf("  1 2 3\n");
		for (int i=1;i<=3;i++) {
			printf("%d ",i);
			for (int j=1;j<=3;j++)
				printf("%c ",state[i][j]==0?'.':(state[i][j]==1?'o':'x'));
			printf("\n");				
		}
		if (rank()) {
			if (rank()==1) printf("You lose\n");
				else printf("You win\n");
			system("pause");
			return 0;
		} else if (checkdraw()) {
			printf("Draw\n");
			system("pause");
			return 0;
		}
		printf("Please select next move(row,column): ");
		int x,y; cin>>x>>y;
		if (state[x][y]==0) {
			state[x][y]=-1;
			And_Or_Tree_Search(zip(),true);
		} else {
			printf("Occupied!\n");
		}
	}
}

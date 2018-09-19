#include<iostream>
#include<cstdio>
#include<cstring>
#include<string>
#include<queue>
using namespace std;
int pow[10]={1,1,2,6,24,120,720,5040,40320,362880}; 
int map[4][4]; char c;
int mx[4]={-1,0,1,0};
int my[4]={0,-1,0,1};
char mv[4]={'u','l','d','r'};
bool visit[400000]={false};

struct Node {
	int now;
	int step;
	string opt;
}temp;

void swap(int &a,int &b)
{
	int t=a; a=b; b=t;
}

int zip(int d[4][4])
{
	int a[10];
	for (int i=1;i<=9;i++)
		a[i]=d[(i-1)/3+1][(i-1)%3+1];
    int x=0;
    for (int i=1;i<=8;i++) {
        int cnt=0;  
        for (int j=i+1;j<=9;j++) 
            if (a[j]<a[i]) cnt++;
        x+=pow[9-i]*cnt; 
    }
    return x;
}

void unzip(int x,int to[4][4]){
	int cnt,label[10];
	for (int i=1;i<=9;i++) label[i]=1;
	for (int i=1;i<=9;i++) {
		cnt=x/pow[9-i];
		x=x%pow[9-i];
		for (int j=1;j<=9;j++){
			if(!label[j]) continue;
			if(!cnt) { label[j]=0; to[(i-1)/3+1][(i-1)%3+1]=j; break;}
			cnt--;
		}
	}
}

void fxy(int a[4][4],int &x,int &y)
{
	for (int i=1;i<=3;i++)
		for (int j=1;j<=3;j++)
			if (a[i][j]==9) {
				x=i; y=j; return;
			}
}

void bfs()
{
	queue <Node> q;
	temp.now=zip(map); temp.opt=""; visit[temp.now]=true; temp.step=0;
	q.push(temp);
	while (!q.empty())
	{
		Node qnow=q.front();
		q.pop();
		int nowvec[4][4],x,y;
		string optnow=qnow.opt;
		unzip(qnow.now,nowvec);
		//cout<<"Now "<<qnow.step<<" :"<<qnow.now<<endl;
		fxy(nowvec,x,y);
		for (int i=0;i<=3;i++){
			int x1=x+mx[i],y1=y+my[i];
			if (x1>0&&x1<=3&&y1>0&&y1<=3){
				swap(nowvec[x][y],nowvec[x1][y1]);
				int newzip=zip(nowvec);
				if (visit[newzip]==false) {
					temp.now=newzip; temp.opt=qnow.opt+mv[i]; temp.step=qnow.step+1;
					q.push(temp); visit[newzip]=true;
					if (newzip==0) {
						cout<<temp.opt<<endl;
						return;
					}
				}
				swap(nowvec[x][y],nowvec[x1][y1]);
			}
		}
	}
	printf("unsolvable\n");
}

int main()
{
	string s;
	while (getline(cin,s)) {
		memset(visit,0,sizeof(visit));
		int n=0,i=0;
		while (n<=s.length()-1){
			i++; c=s[n]; 
			if (c=='x') map[(i-1)/3+1][(i-1)%3+1]=9;
				else map[(i-1)/3+1][(i-1)%3+1]=c-'0';
			n+=3;
		}
		bfs();
	}
} 

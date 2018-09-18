#include <iostream>
#include <queue>
#include <map>
#include <cmath>
#include <stack>
#include<cstdlib>
using namespace std;

map<int,int>step;
map<int,int>fn;
map<int,int>parent;
stack<int>print;
map<int,bool>visit;
int start[3][3];
int state=0;
int graph[3][3];
int ori[4][2]={{0,1},{0,-1},{1,0},{-1,0}};
struct Node{
	Node(int a,int n) {
		this->state=a; this->fn=n;
	}
	int state;
	int fn;
};
bool operator < (const Node &a,const Node &b) {
	return a.fn > b.fn;
}

priority_queue<Node>q;
int dis(int graph[3][3])
{
    int sum=0;
    for(int i=0;i<3;i++)
    {
        for(int j=0;j<3;j++)
        {
            switch (graph[i][j])
            {
                case 1:sum+=abs(i)+abs(j);
                case 2:sum+=abs(i)+abs(j-1);
                case 3:sum+=abs(i)+abs(j-2);
                case 4:sum+=abs(i-1)+abs(j);
                case 5:sum+=abs(i-1)+abs(j-2);
                case 6:sum+=abs(i-2)+abs(j);
                case 7:sum+=abs(i-2)+abs(j-1);
                case 8:sum+=abs(i-2)+abs(j-2);
            }
        }
    }
    return sum;
}

void unzip(int state)
{
    for(int i=2;i>=0;i--)
    {
        for(int j=2;j>=0;j--)
        {
            graph[i][j]=state%10;
            state=(state-graph[i][j])/10;
        }
    }
}

int zip(int graph[3][3])
{
    state=0;
    for(int i=0;i<3;i++)
    {
        for(int j=0;j<3;j++)
        {
            state=state*10+graph[i][j];
        }
    }
    return state;
}

bool CanSwap(int graph[3][3],int dx,int dy)
{
    for(int i=2;i>=0;i--)
    {
        for(int j=2;j>=0;j--)
        {
            if(graph[i][j]==0&&i+dx<3&&i+dx>=0&&j+dy<3&&j+dy>=0)
            {
                swap(graph[i][j],graph[i+dx][j+dy]);
                return true;
            }
        }
    }
    return false;
}

int bfs()
{
    int temp,head;
    while(!q.empty())
    {
        head=q.top().state;
        temp=step[head];
        for(int i=0;i<4;i++)
        {
            unzip(head);
            if(CanSwap(graph,ori[i][0],ori[i][1]))
            {
                int a=zip(graph);
                if(!visit[a])
                {
                    step[a]=temp+1;
                    fn[a]=step[a]+dis(graph);
                    q.push(Node(a,fn[a]));
                    parent[a]=head;
                    visit[a]=true;
                    if(a==123456780)
                    {
                        while(a!=-1)
                        {
                            print.push(a);
                            a=parent[a];
                        }
                        return temp+1;
                    }
                }
            }
        }
        q.pop();
    }
    return -1;
}

int main()
{
	freopen("in.txt","r",stdin); freopen("out.txt","w",stdout);
    for(int i=0;i<3;i++)
    {
        for(int j=0;j<3;j++)
        {
            cin>>start[i][j];
            state=state*10+start[i][j];
        }
    }
    if (state==123456780) {
    	printf("0\n");
    	return 0;
	}
    step[state]=0;
    visit[state]=true;
    parent[state]=-1;
    unzip(state);
    q.push(Node(state,dis(graph)));
    
    cout<<bfs();
    int k=1;
    while(!print.empty())
    {
        unzip(print.top());
        cout<<endl;
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                cout<<graph[i][j]<<" ";
            }
        }
        print.pop();
        k++;
    }
    fclose(stdin); fclose(stdout);
    return 0;
}

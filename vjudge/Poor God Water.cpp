#include<iostream>
#include<cstdio>
#include<cstring>
using namespace std;
long long trans[9][9]=
{
	{0,0,0,0,0,1,0,1,0},
	{1,0,1,0,0,0,0,0,0},
	{1,0,0,1,0,0,0,0,0},
	{0,0,0,0,1,0,1,0,0},
	{0,1,0,0,0,1,0,1,0},
	{0,0,0,0,1,0,1,0,1},
	{0,0,0,0,1,0,0,0,1},
	{0,1,0,0,0,1,0,0,0},
	{0,0,1,1,0,0,0,0,0}
};
long long res1[9][9];
long long start[9]={2,2,2,2,3,3,2,2,2};

void Mul(long long a[9][9],long long b[9][9],long long save[9][9])
{
	long long res[9][9];
	memset(res,0,sizeof(res));
	for (int i=0;i<9;i++)
		for (int j=0;j<9;j++) {
			for (int k=0;k<9;k++){
				res[i][j]+=a[i][k]*b[k][j];
				res[i][j]%=1000000007;
			}
		}
	for (int i=0;i<9;i++)
		for (int j=0;j<9;j++)	
			save[i][j]=res[i][j];
}
void Mul1(long long a[9][9],long long b[9])
{
	int temp[9]={0};
	for (int i=0;i<9;i++){
		for (int k=0;k<9;k++) {
			temp[i]+=(a[i][k]*b[k]);
			temp[i]%=1000000007;
		}
	}
	for (int i=0;i<9;i++)
		b[i]=temp[i];
}
long long ksm(long long n)
{
	long long temp[9][9];
	long long  start1[9];
	for (int i=0;i<9;i++)
		for (int j=0;j<9;j++)
			temp[i][j]=trans[i][j];
	for (int i=0;i<9;i++)
		start1[i]=start[i];
	while (n) {
		if (n&1) Mul(temp,res1,res1);
		Mul(temp,temp,temp);
		n>>=1;
	}
	Mul1(res1,start1);
	long long sum=0;
	for (int i=0;i<9;i++) {
		sum+=start1[i];
		sum%=1000000007;
	}
	return sum;
}

int main()
{
	freopen("out.txt","w",stdout);
	for (int k=1;k<=10000;k++){
		memset(res1,0,sizeof(res1));
		for (int i=0;i<9;i++) res1[i][i]=1; 
		long long n;
		n=k;
		if (n==1) cout<<3<<endl;
			else if (n==2) cout<<9<<endl;
				else cout<<ksm(n-3)<<endl;
	}
	fclose(stdout);
}

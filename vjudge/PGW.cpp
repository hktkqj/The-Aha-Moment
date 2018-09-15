#include<iostream>
#include<cstdio>
#include<cstring>
#define LL long long
using namespace std;
const int maxn = 9;
const int mod = 1e9+7;
LL convert[9][9]={
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
struct Matrix{
    LL a[maxn][maxn];
    void init(){
        memset(a, 0, sizeof(a));
        for(int i=0;i<maxn;++i){
            a[i][i]=1;
        }
    }
};
Matrix mul(Matrix a, Matrix b){
    Matrix ans;
    for(int i=0;i<maxn;++i){
        for(int j=0;j<maxn;++j){
            ans.a[i][j] = 0;
            for(int k=0;k<maxn;++k){
                ans.a[i][j] += a.a[i][k] * b.a[k][j];
                ans.a[i][j] %= mod;
            }
        }
    } 
    return ans;
}

Matrix qpow(Matrix a, LL n){
    Matrix ans;
    ans.init();
    while(n){
        if(n&1) ans = mul(ans, a);
        a = mul(a, a);
        n /= 2;
    } 
    return ans;
}


int main(){
	freopen("out1.txt","w",stdout);
	for (int i=1;i<=10000;i++)
	{
		LL n;
		n=i;
		if (n==1)
		{
			cout<<3<<endl;
			continue;
		}
		if (n==2)
		{
			cout<<9<<endl;
			continue;
		}
		Matrix a;
		for (int i=0;i<maxn;i++) for (int j=0;j<maxn;j++) a.a[i][j]=convert[i][j];
	    Matrix ans = qpow(a, n-3); 
	    long long vec[]={2,2,2,2,3,3,2,2,2};
	    for (int i=0;i<maxn;i++)
	    {
	    	for (int j=0;j<maxn;j++)
	    	{
	    		ans.a[j][i]=ans.a[j][i]*vec[i]%mod;
			}
		}
/*		for (int i=0;i<maxn;i++)
	    {
	    	for (int j=0;j<maxn;j++) cout<<ans.a[i][j]<<" ";
	    	cout<<endl;
		}*/
		LL sum=0;
		for (int i=0;i<maxn;i++)
		{
			for (int j=0;j<maxn;j++) sum=(sum+ans.a[i][j])%mod;
//			cout<<sum<<endl;
		}
		cout<<sum<<endl;
	}
    
    return 0;
}

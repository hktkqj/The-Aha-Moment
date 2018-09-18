#include<iostream>
#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<ctime>
#include<queue>
using namespace std;
#define MAX_HEIGHT 90
#define MAX_WIDTH 120

class Board {
	private :
		int Board_Width;
		int Board_Height;
		int Mine_Number;
		bool First_Click;
		bool Opened_Check[MAX_HEIGHT][MAX_WIDTH];
		//Opened_Check : False-Not opened, True-Opened
		int Board_Map[MAX_HEIGHT][MAX_WIDTH];
		//BoardMap : 0-space(no mine around), -1-(mine), -2-(flag), (1~8)-around mine number
		const int mx={0,0,1,-1};
		const int my={1,-1,0,0}

	public :
		Board(int width, int height, int minenum) {
			std::memset(Opened_Check, 0, sizeof(Opened_Check));
			std::memset(Board_Map, 0, sizeof(Board_Map));
			Board_Width = width;
			Board_Height = height;
			Mine_Number = minenum;
			First_Click = true;
			//Initialize();
		}

		void Initialize() {
			int DeployedMine = 0, PutX, PutY;
			srand((int)time(NULL));
			while (DeployedMine < Mine_Number) {
				PutX = rand() % Board_Width + 1;
				PutY = rand() % Board_Height + 1;
				if (Board_Map[PutY][PutX] == 0) {
					Board_Map[PutY][PutX] = -1;
					++DeployedMine;
				}
			}
			for (int i=1;i<=Board_Height;i++)
				for (int j=1;j<=Board_Width;j++) 
					if (Board_Map[i][j] == 0) {
						int Cnt = 0;
						for (int mx = -1; mx <= 1; mx++)
							for (int my = -1; my <= 1; my++)
								if ((mx != 0 || my != 0) && (i + mx >= 1) && (i + mx <= Board_Height) && (j + my >= 1) && (j + my <= Board_Width) && Board_Map[i + mx][j + my] == -1)
									++Cnt;
						Board_Map[i][j] = Cnt;
					}
		}

		void ShowBoard() {
			for (int i=1;i<=Board_Height;i++) {
				for (int j=1;j<=Board_Width;j++)
					printf("%c ",Board_Map[i][j]==0?'_':(Board_Map[i][j]==-1?'*':(char)(Board_Map[i][j]+'0')));
				printf("\n");
			}
		}
		
		void ClickOn(int x,int y) {
			if (Opened[x][y])
				return;
			for (int i=0;i<=3;i++){
				int x1=x+mx[i],y1=y+my[i];
				
			}
			
		}

};

int main()
{
	Board Game(10,10,10);
	Game.ShowBoard();
}

package solutionGenerator;

import java.util.Random;

import util.Algorithms;

public class LatinSquares {
	
	public static void latinSquare(int dest[][]){
		for (int i = 0; i < 3; i++){
			for (int j = 0; j < 3; j++)
				dest[i][j] = -1;
		}
		int permThree[] = new int[3];
		Algorithms.permutation(permThree, 3);
		for (int i = 0; i < 3; i++)
			dest[i][permThree[i]] = 2;
		
		int d1 = Algorithms.sample(2);
		int d2 = 1 - d1;
		
		int x = 0, y = 0, x1 = 0, y1 = 0, x2 = 0, y2 = 0;
		int x3 = 0, y3 = 0, x4 = 0, y4 = 0;
		for (int i = 0; i < 3; i++){
			if (dest[0][i] == -1){
				y = i;
				break;
			}
		}
		
		dest[x][y] = d1;
		for (int i = 0; i < 3; i++){
			if (dest[i][y] == -1)
				x1 = i;
		}
		y1 = y;
		
		for (int i = 0; i < 3; i++){
			if (dest[0][i] == -1)
				y2 = i;
		}
		x2 = 0;
		
		dest[x1][y1] = d2;
		dest[x2][y2] = d2;
		
		for (int i = 0; i < 3; i++){
			if (dest[x1][i] == -1)
				y3 = i;
		}
		x3 = x1;
		
		for (int i = 0; i < 3; i++){
			if (dest[i][y2] == -1)
				x4 = i;
		}
		y4 = y2;
		
		dest[x3][y3] = d1;
		dest[x4][y4] = d1;
		
		for (int i = 0; i < 3; i++){
			if (dest[i][y3] == -1)
				dest[i][y3] = d2;
			
			if(dest[x4][i] == -1)
				dest[x4][i] = d2;
		}
	}
	
	
	public static void main(String args[]){
		
		int dest[][] = new int [3][3];
		latinSquare(dest);
		
		for (int i = 0; i < 3; i++){
			for (int j = 0; j < 3; j++)
				System.out.print(Integer.toString(dest[i][j]) + ' ');
			System.out.print("\n");
		}
		
	}
}

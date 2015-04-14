package util;

import java.util.Random;

public class Algorithms {

	public static int sample(int n) {
		Random rand = new Random();
		return rand.nextInt(n);
	}
	
	public static void permutation(int dest[], int n){
			
			Random rand = new Random();
			
			for (int i = 0; i < n; i++)
				dest[i] = -1;
			
			for (int i = 0; i < n; i++){
				int randno = rand.nextInt(n - i);
				int j = 0;
				while (true) {
					if (dest[j] == -1)
						randno--;
					if (randno < 0)
						break;
					j = (j+1)%n;
				}
				dest[j] = i;
			}
		}
	
	public static void copy(int dest1[][], int dest2[][], int n){
		for (int i = 0; i < n; i++){
			for (int j = 0; j < n; j++)
				dest1[i][j] = dest2[i][j];
		}
	}
	
	public static void copy(int dest1[][], int dest2[][], int x, int y, int n){
		for (int i = 0; i < n; i++){
			for (int j = 0; j < n; j++)
				dest1[x + i][y + j] = dest2[i][j];
		}
	}
	
	public static void copyRow(int dest1[][], int dest2[][], int row1, int row2, int n) {
		for (int i = 0; i < n; i++)
			dest1[row1][i] = dest2[row2][i];
	}
	
	public static void copyColumn(int dest1[][], int dest2[][], int col1, int col2, int n) {
		for (int i = 0; i < n; i++)
			dest1[i][col1] = dest2[i][col2];
	}
	
	public static void transpose(int dest[][], int n){
		for (int i = 0; i < n; i++){
			for (int j = 0; j < i; j++){
				int temp = dest[i][j];
				dest[i][j] = dest[j][i];
				dest[j][i] = temp;
			}
		}
	}
	
}

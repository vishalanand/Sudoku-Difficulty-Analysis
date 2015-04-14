package solutionGenerator;

import static org.junit.Assert.*;

import org.junit.Test;

import util.Algorithms;

public class LatinSquaresTest {
	
	private static boolean compare(int dest1[][], int dest2[][], int n){
		for (int i = 0; i < n; i++){
			for (int j = 0; j < n; j++)
				if (dest1[i][j] != dest2[i][j])
					return false;
		}
		
		return true;
	}
	
	@Test
	public void test() {
		
		int array[][][] = new int[12][3][3];
		int counts[] = new int[12];
		int n = 0;
		
		for (int z = 0; z < 12000; z++){
			
			int dest[][] = new int[3][3];
			LatinSquares.latinSquare(dest);
			
			boolean status = false;
			
			int i;
			for (i = 0; i < n; i++){
				if (compare(dest, array[i], 3)){
					status = true;
					break;
				}
			}
			
			if (status)
				counts[i]++;
			else {
				Algorithms.copy(array[n], dest, 3);
				n++;
			}			
		}
		
		System.out.println("All the 12 numbers should be close to 1000.");
		for (int i = 0; i < 12; i++)
			System.out.print(Integer.toString(counts[i]) + ' ');
		
	}

}

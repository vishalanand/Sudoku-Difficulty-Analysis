package solutionGenerator;

import util.Algorithms;

public class SolutionGenerator {
	
	public static int[][] generate(){
		
		int dest[][] = new int[9][9];
		
		latinGenerate(dest);
		jumbleRows(dest);
		
		rows(dest, 0);
		rows(dest, 1);
		rows(dest, 2);
		
		for (int i = 0; i < 12; i++){
			int grp = Algorithms.sample(3);
			if (Algorithms.sample(2) == 1)
				rows(dest, grp);
			else
				cols(dest, grp);
		}
		
		if (Algorithms.sample(2) == 1)
			Algorithms.transpose(dest, 9);
		
		mapping(dest);
		
		return dest;
	}

	public static void mapping(int dest[][]){
		
		int perm[] = new int[9];
		Algorithms.permutation(perm, 9);
		
		for (int i = 0; i < 9; i++){
			for (int j = 0; j < 9; j++){
				int elem = dest[i][j];
				elem = perm[elem - 1] + 1;
				dest[i][j] = elem;
			}
		}
	}
	
	public static void rows(int dest[][], int grp) {
		int perm[] = new int[3];
		int temp[][] = new int[3][9];
		
		Algorithms.permutation(perm, 3);
		
		Algorithms.copyRow(temp, dest, 0, 3*grp, 9);
		Algorithms.copyRow(temp, dest, 1, 3*grp + 1, 9);
		Algorithms.copyRow(temp, dest, 2, 3*grp + 2, 9);
		
		Algorithms.copyRow(dest, temp, 3*grp + perm[0], 0, 9);
		Algorithms.copyRow(dest, temp, 3*grp + perm[1], 1, 9);
		Algorithms.copyRow(dest, temp, 3*grp + perm[2], 2, 9);
	}
	
	public static void cols(int dest[][], int grp) {
		int perm[] = new int[3];
		int temp[][] = new int[9][3];
		
		Algorithms.permutation(perm, 3);
		
		Algorithms.copyColumn(temp, dest, 0, 3*grp, 9);
		Algorithms.copyColumn(temp, dest, 1, 3*grp + 1, 9);
		Algorithms.copyColumn(temp, dest, 2, 3*grp + 2, 9);
		
		Algorithms.copyColumn(dest, temp, 3*grp + perm[0], 0, 9);
		Algorithms.copyColumn(dest, temp, 3*grp + perm[1], 1, 9);
		Algorithms.copyColumn(dest, temp, 3*grp + perm[2], 2, 9);
	}
	
	public static void jumbleRows(int dest[][]){
		int temp[][] = new int[9][9];
		Algorithms.copyRow(temp, dest, 0, 0, 9);
		Algorithms.copyRow(temp, dest, 3, 1, 9);
		Algorithms.copyRow(temp, dest, 6, 2, 9);
		Algorithms.copyRow(temp, dest, 1, 3, 9);
		Algorithms.copyRow(temp, dest, 4, 4, 9);
		Algorithms.copyRow(temp, dest, 7, 5, 9);
		Algorithms.copyRow(temp, dest, 2, 6, 9);
		Algorithms.copyRow(temp, dest, 5, 7, 9);
		Algorithms.copyRow(temp, dest, 8, 8, 9);
		
		Algorithms.copy(dest, temp, 9);
	}
	
	public static void latinGenerate(int dest[][]) {
		
		int template[][] = new int[3][3];
		LatinSquares.latinSquare(template);
		
		for (int i = 0; i < 9; i++)
			for (int j = 0; j < 9; j++)
				dest[i][j] = -1;
		
		for (int i = 0; i < 3; i++){
			for (int j = 0; j < 3; j++){
				int latin[][] = new int[3][3];
				LatinSquares.latinSquare(latin);
				int mul = template[i][j];
				for (int x = 0; x < 3; x++){
					for (int y = 0; y < 3; y++)
						latin[x][y] = 3*mul + latin[x][y] + 1;
				}
				
				Algorithms.copy(dest, latin, 3*i, 3*j, 3);
			}
		}
	}
	
	public static void main(String args[]){
		
		int dest[][] = generate();
		
		for(int i = 0; i < 9; i++){
			for (int j = 0; j < 9; j++)
				System.out.print(Integer.toString(dest[i][j]) + ' ');
			System.out.print("\n");
		}
		
	}
	
}

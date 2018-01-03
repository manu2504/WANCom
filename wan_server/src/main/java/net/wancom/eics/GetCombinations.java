package net.wancom.eics;

import java.util.ArrayList;
import java.util.Stack;



public class GetCombinations {


    /*TODO: Get the distance of every link save in (an array)  that we want to test for combinations with a constraint*/
    private Stack<Integer> stack = new Stack<Integer>();
    private int sum=0;
    public void sumLinkCombinations(ArrayList<Integer> distanceBetweenLinks, int constraint){
        /*check if the sum of different combinations- meet the constraint*/
        if(sum<constraint){
            print(stack);
        }
        for (int i =0;i<distanceBetweenLinks.size(); i++){
            if (sum + distanceBetweenLinks.get(i)<constraint){
                stack.push(distanceBetweenLinks.get(i));
                sum += distanceBetweenLinks.get(i);
                sumLinkCombinations(distanceBetweenLinks,i+1);
                sum -=(Integer) stack.pop();
            }
        }
    }
    /*print all the summary of the different combinations that meet the constraint*/
    private void print(Stack<Integer> stack) {
        StringBuilder sb = new StringBuilder();
        for (Integer i : stack) {
            sb.append(i).append("+");
        }
        System.out.println(sb.deleteCharAt(sb.length() - 1).toString());
    }



}

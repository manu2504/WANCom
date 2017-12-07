import javafx.scene.input.ScrollEvent;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class DHeap {
    private Map<String, Vertex> heap;
    private int size;
    private int d;

    public DHeap(int d, Map<String, Vertex> objects) {
        this.d = d;
        this.heap=new HashMap<String, Vertex>(objects) ;
        this.size = objects.size();
        for(int i=this.size-1;i>=0;i--)
            dive(i);
    }



    public int getSize(){
        return size;
    }
    /*
    public Vertex[] getAll(){
        return heap;
    }
    */

    private void swap(int a, int b){
        Vertex[] values = (Vertex [])heap.values().toArray();
        Vertex t= values[a];
        values [a] =values[b];
        values[b]=t;
        values[a].setNode(a);
        values[b].setNode(b);

    }


    private double keyOf(int a){
        Object[] values = heap.values().toArray();

        return ((Vertex)values[a]).getKey();

    }


    private void emersion(int a){
        int p=(a-1)/d;
        while((a!=0)&&(keyOf(p)>keyOf(a))){
            swap(a,p);
            a=p;
            p=(a-1)/d;
        }
    }


    private void dive(int a){
        int ch=minChild(a);
        while((ch!=-1)&&(keyOf(ch)<keyOf(a))){
            swap(ch,a);
            a=ch;
            ch=minChild(a);
        }
    }

    private int minChild(int a){
        if((d*a+1)>=size)
            return -1;
        int min=d*a+1;
        for(int i=d*a+2;i<Math.min(size, d*a+d+1);i++){
            if(keyOf(i)<keyOf(min))
                min=i;
        }
        return min;
    }


    public void delete(int a){
        Object[] values = heap.values().toArray();
        values[a]=(Vertex)values[size-1];
        size--;
        if((a!=0)&&(keyOf(a)<keyOf((a-1)/3)))
            emersion(a);
        else
            dive(a);
    }
    public Vertex getMin(){
        Object[] values = heap.values().toArray();
        Vertex min=(Vertex)values[0];
        delete(0);
        return min;
    }
    public double getMinKey()
    {
        return keyOf(0);
    }

    public void decKey(int a, double val){
        Object[] values = heap.values().toArray();
        if(keyOf(a)>val){
            ((Vertex)values[a]).setDistance(val);
            emersion(a);
        }
    }


}
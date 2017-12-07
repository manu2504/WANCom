
package model;


public class DHeap {
	private Vertex[] heap;
	private int size;
	private int d;
	public DHeap(int d, Vertex[] objects){
		super();
		this.d=d;
		this.heap=objects.clone();
		this.size=objects.length;
		for(int i=heap.length-1;i>=0;i--)
			dive(i);
	}
	public int getSize(){
		return size;
	}
	public Vertex[] getAll(){
		return heap;
	}
	private void swap(int a, int b){
		Vertex t=heap[a];
		heap[a]=heap[b];
		heap[b]=t;
		heap[a].setNode(a);
		heap[b].setNode(b);
	}
	private int keyOf(int a){
		return heap[a].getKey();
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
	public void add(Vertex v){
		heap[size]=v;
		emersion(size);
		size++;
	}
	public void delete(int a){
		heap[a]=heap[size-1];
		size--;
		if((a!=0)&&(keyOf(a)<keyOf((a-1)/3)))
			emersion(a);		
		else
			dive(a);
	}
	public Vertex getMin(){
		Vertex min=heap[0];
		delete(0);
		return min;
	}
	public int getMinKey(){
		return keyOf(0);
	}
	public void decKey(int a, int val){
		if(keyOf(a)>val){
			heap[a].setDistance(val);
			emersion(a);
		}
	}
}

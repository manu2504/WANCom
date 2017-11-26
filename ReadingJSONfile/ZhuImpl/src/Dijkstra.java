import java.util.LinkedList;

public class Dijkstra {

    public static LinkedList<Integer> doDijkstra(Graph graph, int from, int to){
        DHeap d=new DHeap(3, graph.getAll());
        d.decKey(graph.getVertex(from).getNode(), 0);
        while((!graph.getVertex(to).isVisited())&&(d.getSize()>0)){
            Vertex cur = d.getMin();
            for(Edge e:cur.getEdges()){
                Vertex end = graph.getVertex(e.getEndPoint());
                if(!end.isVisited()){
                    if(end.getDistance()>(cur.getDistance()+e.getWeight())){
                        d.decKey(end.getNode(), cur.getDistance()+e.getWeight());
                        end.setParent(cur.getNum());
                    }
                }
            }
            cur.markVisited();
        }

        if(graph.getVertex(to).getDistance()!=Integer.MAX_VALUE){
            int v=to;
            LinkedList<Integer> res=new LinkedList<>();
            while(v!=-1){
                res.addFirst(v);
                v=graph.getVertex(v).getParent();
            }
            res.addLast(graph.getVertex(to).getDistance());
            return res;
        }
        return null;



    }


}


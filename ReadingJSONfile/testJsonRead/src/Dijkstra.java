import java.util.LinkedList;

public class Dijkstra {

    /**have t*/
    public static LinkedList<String> doDijkstra(Graph graph, String src, String dst){
       DHeap d=new DHeap(3, graph.getAll());
        d.decKey(graph.getVertex(src).getNode(), 0);
        while((!graph.getVertex(dst).isVisited())&&(d.getSize()>0)){
            Vertex cur = d.getMin();
            for(Edge e:cur.getEdges()){
                //before  Vertex end = graph.getVertex(e.getEndPoint());
                Vertex end = graph.getVertex(e.getEndPoint().toString());
                if(!end.isVisited()){
                    if(end.getDistance()>(cur.getDistance()+e.getWeight())){
                        d.decKey(end.getNode(), cur.getDistance()+e.getWeight());
                        //before end.setParent(cur.getNum())
                        end.setParent(cur.getId());
                    }
                }
            }
            cur.markVisited();
        }

        if(graph.getVertex(dst).getDistance()!=Double.MAX_VALUE){
            String  v=dst;
            LinkedList<String> res=new LinkedList<>();
            while(v!=""){
                res.addFirst(v);
                v=graph.getVertex(v).getParent();
            }
            res.addLast(graph.getVertex(dst).getDistance().toString());
            return res;
        }
        return null;
    }


}


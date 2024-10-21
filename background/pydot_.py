#### 
####  error : FileNotFoundError: [Errno 2] No such file or directory: 'dot'
#### 😀 sudo apt install graphviz

import pydot
import datetime

def main(plot_datas, ping_results) -> str:
    graph = pydot.Dot("my_graph", graph_type="digraph", bgcolor="white")

    ### 😀 그냥 zip으로 for 하면, 2번째 loop가 안돌아감. ㅜㅜ;;
    # plot_datas = list(plot_datas_zip)

    for host in plot_datas:
        try:
            host:dict #{'id': 1, 'Category': '성남[7.xxx]    ', 'Category_순서': 10000, 'IP_주소': '192.168.7.1', 'host_이름': 'Gateway      ', 'host_설명': None, 'MAC_주소': '      ', '비고': '      ', 'Group': '성남', '상위IP': '192.168.7.1'}
            label_txt = f"{host.get('host_이름')} \n ({host.get('IP_주소')})"
            nodeName = host.get('IP_주소').replace('.', '_')
            graph.add_node ( pydot.Node( nodeName , label = label_txt , style='filled', fillcolor=get_color(host, ping_results)) )
        except Exception as e:
            print ( 'Node Generation error :', e)

    for host in plot_datas:
        try:
            host:dict #{'id': 1, 'Category': '성남[7.xxx]    ', 'Category_순서': 10000, 'IP_주소': '192.168.7.1', 'host_이름': 'Gateway      ', 'host_설명': None, 'MAC_주소': '      ', '비고': '      ', 'Group': '성남', '상위IP': '192.168.7.1'}
            nodeName_상위 = host.get("상위IP", '').replace('.', '_' )
            nodeName_하위 = host.get('IP_주소', '').replace('.', '_')

            color = get_color(host, ping_results)
            if not nodeName_상위 or not nodeName_하위 :
                continue
            graph.add_edge ( pydot.Edge ( nodeName_상위, nodeName_하위, color= color ) )
        except Exception as e:
            print ( 'Edge Generation error:', e)

    fileName = datetime.datetime.now().strftime('%Y-%m-%dT%H:%m:%s')
    filepath = f"./network결과/{fileName}.png"
    filepath = f"./network결과/{fileName}.svg"

    graph.write_svg(filepath)
    
    return resize_by_CV2(filepath )
    # # Add nodes
    # my_node = pydot.Node("a", label="Foo")
    # graph.add_node(my_node)
    # # Or, without using an intermediate variable:
    # graph.add_node(pydot.Node("b", shape="circle"))

    # # Add edges
    # my_edge = pydot.Edge("a", "b", color="blue")
    # graph.add_edge(my_edge)
    # # Or, without using an intermediate variable:
    # graph.add_edge(pydot.Edge("b", "c", color="blue"))


def resize_by_CV2(filepath:str) -> str:
    return filepath
    image = cv2.imread(filepath)
    image = cv2.resize( image, (1000, 700) )
    cv2.imwrite(filepath, image)
    return filepath


def get_color(host:dict, results:list) -> str:
    # print (host, results)
    # result:list #[True, '192.168.7.1', 0.0025288600008934736]
    ERROR_COLOR = 'red'
    DEALY_COLOR = 'orange'
    NORMAL_COLOR = 'blue'

    DELAY_CONDITON = 20

    host_ip = host.get('IP_주소')
    # print ( results, host_ip)
    result:list = list(filter( lambda obj: obj[1] == host_ip, results ))[0]
    # print ( host_ip , '---finded : ',  result )

    if len(result) != 3 : return ERROR_COLOR
    ### float 0.00234... , text ' timed out.'
    if not result[0] : return  ERROR_COLOR

    응답시간:float = result[2] * 1000 ### msec
    return NORMAL_COLOR if 응답시간 < DELAY_CONDITON else DEALY_COLOR

def test():
    # first you create a new graph, you do that with pydot.Dot()
    graph = pydot.Dot(graph_type='graph')

    # the idea here is not to cover how to represent the hierarchical data
    # but rather how to graph it, so I'm not going to work on some fancy
    # recursive function to traverse a multidimensional array...
    # I'm going to hardcode stuff... sorry if that offends you

    # let's add the relationship between the king and vassals
    for i in range(3):
        # we can get right into action by "drawing" edges between the nodes in our graph
        # we do not need to CREATE nodes, but if you want to give them some custom style
        # then I would recomend you to do so... let's cover that later
        # the pydot.Edge() constructor receives two parameters, a source node and a destination
        # node, they are just strings like you can see
        edge = pydot.Edge("king", "lord%d" % i)
        # and we obviosuly need to add the edge to our graph
        graph.add_edge(edge)

    # now let us add some vassals
    vassal_num = 0
    for i in range(3):
        # we create new edges, now between our previous lords and the new vassals
        # let us create two vassals for each lord
        for j in range(2):
            edge = pydot.Edge("lord%d" % i, "vassal%d" % vassal_num)
            graph.add_edge(edge)
            vassal_num += 1

    # ok, we are set, let's save our graph into a file
    graph.write_png('example1_graph.png')

if __name__ == '__main__':
#    main()
    test()
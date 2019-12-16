# def drawActionSeqGantt(self):
#     '''
#     '''
#     self.checkActionSeq()
#     multiPerm = self._seq.convert2MultiPerm(self._robNum)
#     print(multiPerm)
#     actionRobLst = [[] for x in range(self._robNum)]
#     for act in self._seq:
#         actionRobLst[act.robID].append(act)
#     df = []
#     for robID in range(self._robNum):
#         for ind in range(0,len(actionRobLst[robID]),2):
#             dic = dict(Task = 'rob' + str(robID),
#                        Start = actionRobLst[robID][ind].eventTime,
#                        Finish = actionRobLst[robID][ind + 1].eventTime,
#                        Resource = 'Task' + str(actionRobLst[robID][ind].taskID))
#             df.append(dic)
#         # if robID > 1:
#         #     break
#     colorLst = cl.scales[str(self._taskNum)]['qual']['Paired']
#     colorDic = dict()
#     for taskID in range(self._taskNum):
#         colorDic['Task' + str(taskID)] = colorLst[taskID]
#     print(colorDic)
#     print(df)
#     # print(actionRobLst)
#     # exit()
#     # for act in self._seq:
#     #     pass
#     #     # df.append(dict(Task = ''))
#     # for robID in range(self._robNum):
#     #     df.append(dict(Task = 'rob'+ str(robID), Start = 1, Finish = 5))
#     # fig = ff.create_gantt(df, colors=colorDic, index_col= 'Resource', show_colorbar=True, group_tasks=True)
#     fig = ff.create_gantt(df,  index_col= 'Resource', show_colorbar= True, group_tasks= True)
#     fig['layout']['xaxis']['type'] = 'linear'
#     fig['layout']['xaxis']['zeroline'] = True
#     fig.show()
# def drawTaskScatter(self):
#     self.checkActionSeq()
#     multiPermTask = [[] for x in range(self._taskNum)]
#     # fig = go.Figure()
#     fig = make_subplots(rows= self._taskNum, cols=1)
#
#     for taskID in range(self._taskNum):
#         for act in self._seq:
#             if act.taskID == taskID:
#                 multiPermTask[taskID].append(act)
#         # print(multiPermTask[taskID])
#         for uint in multiPermTask[taskID]:
#             print(uint)
#         # exit()
#         taskStateSeq = multiPermTask[taskID]
#         task_state = self._taskStateLst[taskID]
#         task_rate = self._taskRateLst[taskID]
#         task_time = 0
#         xLst = []
#         yLst = []
#         for taskStatePnt in taskStateSeq:
#             xarray = np.linspace(task_time,taskStatePnt.eventTime,100)
#             for x in xarray:
#                 xLst.append(x)
#                 y = math.log(task_state*math.exp((x-task_time)*task_rate))
#                 yLst.append(y)
#             # taskStatePnt.eventTime
#             task_state =  task_state*math.exp((taskStatePnt.eventTime - task_time)*task_rate)
#             if taskStatePnt.eventType == EventType.leave:
#                 task_rate = task_rate + self._robAbiLst[taskStatePnt.robID]
#             else:
#                 task_rate = task_rate - self._robAbiLst[taskStatePnt.robID]
#             task_time = taskStatePnt.eventTime
#             if math.isclose(task_state,self._threhold):
#                 break
#             # anno = go.layout.Annotation(x = xLst[-1] + np.random.randint(-10,10), y = yLst[-1] + np.random.randint(-10,10), text='rob' + str(taskStatePnt.robID))
#             # fig.update_layout()
#             # go.layout.
#             # print(xLst[-1], yLst[-1])
#             # fig.add_annotation(anno)
#         scatter = go.Scatter(x= xLst , y = yLst ,mode='lines', name = 'task' + str(taskID))
#         fig.add_trace(scatter,row = taskID + 1, col = 1 )
#         fig.update_xaxes(range = [0, self._seq[-1].eventTime], row = taskID + 1, col = 1)
#         # fig.update_annotations(dict(xref="x",yref="y"))
#     fig.show()
#     # exit()
#     print(multiPermTask)
#
#     pass
# def drawTaskDependence(self):
#     multiPerm = self._seq.convert2MultiPerm(self._robNum)
#     print(multiPerm)
#     d_graph = nx.DiGraph()
#     for perm in multiPerm:
#         perm.reverse()
#         d_graph.add_path(perm)
#     labels = {}
#     for taskID in range(self._taskNum):
#         labels[taskID] = str(taskID)
#         print(taskID, d_graph.out_degree(taskID), d_graph.in_degree(taskID))
#     nx.draw(d_graph, pos = nx.planar_layout(d_graph), labels = labels)  # networkx draw()
#
#     plt.show()  # pyplot draw()
#         # for i in range(len(perm) - 1):
#
#     # d_graph.degree()

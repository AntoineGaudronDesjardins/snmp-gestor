from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType
from modules.utils import formatter
from modules.snmp.mibNode import MibNode


class Table:
    def __init__(self, snmpEngine, mibName, tableName):
        self.engine = snmpEngine
        self.mibs = snmpEngine.mibViewController
        self.ref = MibNode(self.engine, (mibName, tableName))
        self.columns = []
        self.indexes = []
        self.rows = []
    

    ######################################################################################
    ############################### Data specific methods ################################
    ######################################################################################
    def pullData(self, *columns, startIndex=(), maxRepetitions=1000, auth=None):
        self.columns = []
        self.indexes = []
        self.rows = []
        self.columns = self._getAllColumns(columns)

        includeFirst = (startIndex != ())
        mibName, _, _ = self.ref[0].getMibSymbol()
        reqColumns = [ObjectType(ObjectIdentity(mibName, column, *startIndex)) for column in self.columns]
        self.rows, self.indexes = self.engine.getTable(reqColumns, maxRepetitions, auth, includeFirst, self._check)
        return self

    
    def getRows(self, startIndex=(), maxRepetitions=1000):
        index = 0
        if startIndex in self.indexes:
            index = self.indexes.index(startIndex)
        return self.rows[index:index+maxRepetitions]


    def getColumns(self, *columns):
        indexes = [i for i, column in enumerate(self.columns) if column in columns]
        return [[row[i] for i in indexes] for row in self.rows]
        
    
    def getNext(self, auth=None):
        last = self.rows[-1][-1]
        varBind = self.engine.getNext(last, auth)
        if varBind:
            return MibNode(self.engine, varBind)


    def setRow(self, index, varBinds, auth=None):
        mib, _, _ = self.ref[0].getMibSymbol()
        instances = [ObjectType(ObjectIdentity(mib, col, *index), val) for col, val in varBinds]
        newRow = self.engine.setTableRow(instances, auth)
        if newRow:
            if index in self.indexes:
                i = self.indexes.index(index)
                self.rows[i] = newRow
            else:
                self.indexes.append(index)
                self.rows.append(newRow)
            return self

    
    def setColumn(self, column, value, auth=None):
        mib, _, _ = self.ref[0].getMibSymbol()
        if not(self.indexes):
            self.pullData()
        instances = [ObjectType(ObjectIdentity(mib, column, *index), value) for index in self.indexes]
        newRow = self.engine.setTableRow(instances, auth)
        if newRow and (column in self.columns):
            self.pullData(*self.columns)
    

    @property
    def values(self):
        return [[varBind[1].prettyPrint() for varBind in row] for row in self.rows]


    ######################################################################################
    ################################### Render methods ###################################
    ######################################################################################
    def format(self, pattern, name=True):
        formattedTable = [formatter(self.mib, row, format=pattern) for row in self.rows]
        if name:
            return { self.tableName : formattedTable }
        else:
            return formattedTable
    

    def print(self, index=True, header=True):
        _, tableName, _ = self.ref[0].getMibSymbol()
        if not self.rows:
            return f"Table {tableName} is empty"
        
        elif len(self.rows) == 1:
            rowData = []
            for i, varBind in enumerate(self.rows[0]):
                symb = self.columns[i]
                rowData.append(f"  {symb} = {varBind[1].prettyPrint()} ")
            rowData = '\n'.join(rowData)
            if index:
                printableIndex = [str(index) for index in self.indexes[0]]
                rowData = f"  index = {'.'.join(printableIndex)} \n" + rowData
            return f"\n _{tableName}_ : \n{rowData}"

        else:
            columnsSize = [0 for _ in self.columns]
            if header:
                columnsSize = [len(column) for column in self.columns]
                if index:
                    columnsSize.append(len("index"))
            for j, row in enumerate(self.rows):
                if index:
                    columnsSize[-1] = max(columnsSize[-1], len(",".join([str(i) for i in self.indexes[j]])))
                for i, varBind in enumerate(row):
                    columnsSize[i] = max(columnsSize[i], len(varBind[1].prettyPrint()))
            
            table = []
            if header:
                table.append("| " + " | ".join([col.ljust(columnsSize[i]) for i, col in enumerate(self.columns)]) + " |")
                if index:
                    table[0] = "| " + "index".ljust(columnsSize[-1]) + " " + table[0]
                table.append("|" + "+".join(["-"*(columnSize+2) for columnSize in columnsSize]) + "|")
            for j, row in enumerate(self.rows):
                table.append("| " + " | ".join([varBind[1].prettyPrint().ljust(columnsSize[i]) for i, varBind in enumerate(row)]) + " |")
                if index:
                    table[-1] = "| " + ",".join([str(i) for i in self.indexes[j]]).ljust(columnsSize[-1]) + " " + table[-1]
            tableData = "\n".join(table)

            return f"\n _{tableName}_ : ```\n{tableData}```"
    

    def __repr__(self):
        return self.print()
    

    ######################################################################################
    ################################## Internals methods #################################
    ######################################################################################
    def _getAllColumns(self, columns, auth=None):
        if not columns:
            tableOid = self.ref["oid"]
            columns = []
            index = 1
            args = None
            while not args:
                scalar = MibNode(self.engine, f"{tableOid}.1.{index}")
                _, column, args = scalar.getMibSymbol()
                if args:
                    continue
                index+=1
                
                nextScalar = scalar.getNext(auth)
                if not nextScalar:
                    break
                elif scalar.isParent(nextScalar):
                    columns.append(column)
        return columns
    

    def _check(self, varBinds):
        rowIndex = None
        if not varBinds:
            return False, None
        
        for i, obj in enumerate(varBinds):
            _, symb, index = obj[0].getMibSymbol()
            
            if (not symb in self.columns) or (self.columns.index(symb) != i):
                return False, None
            
            if not rowIndex:
                rowIndex = index
            elif rowIndex != index:
                return False, None
        
        return True, rowIndex
    

    # def __iter__(self):
    #     self.iterIndex = 0
    #     return self
    

    # def __next__(self):
    #     if self.iterIndex >= len(self.rows):
    #         raise StopIteration
    #     self.iterIndex += 1
    #     return [varBind[1].prettyPrint() for varBind in self.rows[self.iterIndex-1]]
    

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.rows[key] 
    

    def __len__(self):
        return len(self.rows)

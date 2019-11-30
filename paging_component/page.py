from django.utils.safestring import mark_safe

class Paging:
    def __init__(self,current_page_number,total_count,per_page_count=10,page_number_show=5,recv_data=None):
        """

        :param current_page_number: 当前页码
        :param total_count: 总数据量
        :param per_page_count: 每页显示多少条  --- 数据
        :param page_number_show:  每页下方显示多少个页码  --- 页码

        start_page_number:起始页码
        end_page_number:结束页码
        """
        self.recv_data = recv_data

        # 传过来是字符串，需要将其转换成整型
        try:
            current_page_number = int(current_page_number)
        except Exception:
            current_page_number = 1

        # 将当前页码保持在中间位置
        half_number = page_number_show//2
        a,b = divmod(total_count,per_page_count)
        # 如果余数不为0，页码总数为商+1
        if b:
            total_page_count = a + 1
        else:
            total_page_count = a


        # 当当前页码小于等于0的时候，默认显示最后一页
        if current_page_number >= total_page_count:
            current_page_number = total_page_count

        # 当当前页码小于等于0的时候，默认显示第一页
        if current_page_number <= 0:
            current_page_number = 1

        # 下方页码的起始页码以及最后页码数
        start_page_number = current_page_number - half_number
        end_page_number = current_page_number + half_number + 1

        # 起始页码小于等于0
        if start_page_number <= 0:
            start_page_number = 1
            end_page_number = page_number_show + 1

        # 最后页码大于总共的页码数
        if end_page_number >= total_page_count:
            start_page_number = total_page_count - page_number_show + 1
            end_page_number = total_page_count + 1

        #
        if total_page_count < page_number_show:
            start_page_number = 1
            end_page_number = total_page_count + 1

        self.current_page_number = current_page_number
        self.per_page_count = per_page_count
        self.total_page_count = total_page_count
        self.start_page_number = start_page_number
        self.end_page_number = end_page_number

    # 本页显示数据的起始数据
    @property
    def start_data_number(self):
        return (self.current_page_number - 1) * self.per_page_count

    # 本页显示数据的最后数据
    @property
    def end_data_number(self):
        return self.current_page_number * self.per_page_count

    # 前端显示页面
    def page_html_func(self):
        page_html = """
                 <nav aria-label="Page navigation">
                  <ul class="pagination">
                    """
        self.recv_data['page'] = 1
        first_page = f"""
                       <li>
                         <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                           <span aria-hidden="true">首页</span>
                         </a>
                       </li>
                       """

        page_html += first_page

        self.recv_data['page'] = self.current_page_number - 1
        previous_page = f"""
                       <li>
                         <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                           <span aria-hidden="true">&laquo;</span>
                         </a>
                       </li>
                        """
        page_html += previous_page

        for i in range(self.start_page_number,self.end_page_number):
            self.recv_data['page'] = i
            if i == self.current_page_number:
                page_html += f'<li class="active"><a href="?{self.recv_data.urlencode()}">{i}</a></li>'
            else:
                page_html += f'<li><a href="?{self.recv_data.urlencode()}">{i}</a></li>'

                # 方式二：
                # page_html += f'<li><a href="?{i}&{self.recv_data.urlencode().replace("page="+str(self.current_page_number)+"&","") if "page" in self.recv_data.urlencode() else self.recv_data.urlencode()}">{i}</a></li>'

        self.recv_data['page'] = self.current_page_number + 1
        next_page = f"""
                       <li>
                             <a href="?{self.recv_data.urlencode()}" aria-label="Next">
                               <span aria-hidden="true">&raquo;</span>
                             </a>
                           </li>
           """
        page_html += next_page

        self.recv_data['page'] = self.total_page_count
        last_page = f"""
                           <li>
                             <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                               <span aria-hidden="true">尾页</span>
                             </a>
                           </li>"""
        page_html += last_page

        page_html += """

                         </ul>
                       </nav>
                   """

        return mark_safe(page_html)
import datetime
from BaseXClient import BaseXClient
from lxml import etree

session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')


def comment(local_id):
    comments = [
        {"name": "Roberto Suben", "comment": "Preferia ver Sol 30 vezes a ter isto", "date": "2020-12-09", "id": "0"},
        {"name": "GilBerto Verde", "comment": "AAAADDDDOORREEEEIIII S2", "date": "2020-12-09", "id": "1"},
        {"name": "Maria Cantil", "comment": "Meh!", "date": "2020-12-09", "id": "2"},
        {"name": "Roberto Suben", "comment": "Preferia ver Sol 30 vezes a ter isto", "date": "2020-12-09", "id": "3"},
        {"name": "GilBerto Verde", "comment": "AAAADDDDOORREEEEIIIIAAAADDDDOORREEEEIIIIAAAADDDDOORREEEEIIII S2",
         "date": "2020-12-09", "id": "4"},
        {"name": "Maria Cantil", "comment": "Meh!", "date": "2020-12-09", "id": "5"},
        {"name": "Roberto Suben", "comment": "Preferia ver Sol 30 vezes a ter isto", "date": "2020-12-09", "id": "6"},
        {"name": "GilBerto Verde", "comment": "AAAADDDDOORREEEEIIII S2", "date": "2020-12-09", "id": "7"},
        {"name": "Maria Cantil", "comment": "Meh!", "date": "2020-12-09", "id": "8"}]

    def_local_id = 2742611  # Aveiro
    query = f'''  
    import module namespace c = "FiveDayForecast.functions";

    c:list_comments({local_id})
                '''
    query2 = session.query(query)
    xml = query2.execute()

    root = etree.XML(xml)
    comments_dict = elem2dict(root)
    comments_str = ""
    if comments_dict:
        print(comments_dict['comment'])
        for r in comments_dict['comment']:
            print(r)
            comments_str += f'''
                                    <div class="col-md-6 mb-4" id="{r["id"]}">
                                        <div class= "card">
                                            <div class="card-body">
                                                <div class="clearfix"">
                                                    <h5 class="float-left">{r["name"]}</h5> 
                                                    <span class="float-right">
                                                        <input type="date" class="form-control" value="{r["date"]}" readonly="True"></input>
                                                    </span>
                                                </div>
                                                <p>{r["text"]}</p>
                                            </div>
                                            <div class="card-footer">
                                                <button type="button" class="btn btn-primary btn-sm btn-block" id="{r["id"]}">Edit</button>
                                                <button type="button" class="btn btn-danger btn-sm btn-block" id="{r["id"]}">Remove</button>
                                            </div>
                                        </div>
                                </div>
                            '''
    return comments_str


def new_comment(local_id, name, data, date):
    query = f'''  
    import module namespace c = "FiveDayForecast.functions";

    c:new_comment(\"{name}\",\"{data}\",\"{date}\",{local_id})
                '''
    query2 = session.query(query)

    query2.execute()


def edit_comment(comment, location_id, id):
    query = f'''  
    import module namespace c = "FiveDayForecast.functions";

    c:edit_comment({comment},{location_id},{id})
                '''
    query2 = session.query(query)

    query2.execute()


def remove_comment(location_id, id):
    query = f'''  
    import module namespace c = "FiveDayForecast.functions";

    c:remove_comment({location_id},{id})
                '''
    query2 = session.query(query)

    query2.execute()


def elem2dict(node):
    """
    Convert an lxml.etree node tree into a dict.
    """
    result = {}

    for element in node.iterchildren():
        # Remove namespace prefix
        key = element.tag.split('}')[1] if '}' in element.tag else element.tag

        # Process element as tree element if the inner XML contains non-whitespace content
        if element.text and element.text.strip():
            value = element.text
        else:
            value = elem2dict(element)
        if key in result:

            if type(result[key]) is list:
                result[key].append(value)
            else:
                tempvalue = result[key].copy()
                result[key] = [tempvalue, value]
        else:
            result[key] = value
    return result

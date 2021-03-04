import datetime
from BaseXClient import BaseXClient
from lxml import etree

session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')


def comment(local_id, forecast=False):
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
        if type(comments_dict['comment']) is dict:
            comments_dict['comment'] = [comments_dict['comment']]
        for r in comments_dict['comment']:
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
                                                <button type="button" class="btn btn-primary btn-sm btn-block" data-toggle="modal" data-target="#EditModal-{r['id']}">Edit</button>
                                                <div class="modal fade" id="EditModal-{r['id']}" tabindex="-1" role="dialog" aria-labelledby="EditModalLabel-{r['id']}" aria-hidden="true">
                                              <div class="modal-dialog" role="document">
                                                <div class="modal-content">
                                                  <div class="modal-header">
                                                    <h5 class="modal-title" id="EditModalLabel-{r['id']}">{r['name']}</h5>
                                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"></button>
                                                  </div>
                                                  <form action="/weather/edit" method="post">
                                                  <div class="modal-body">
                                                    <textarea type="text" name="edit_text" class="form-control" style="max-width: 100%;" placeholder="Comment" spellcheck="True">{r['text']}</textarea>
                                                    <input id="local" name="local" type="hidden" value="{local_id}">
                                                    <input id="edit_id" name="edit_id" type="hidden" value="{r['id']}">
                                                    <input id="edit_forecast" name="edit_forecast" type="hidden" value="{forecast}">
                                                  </div>
                                                  <div class="modal-footer">
                                                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                                    <button type="submit" class="btn btn-primary">Save changes</button>
                                                  </div>
                                                  </form>
                                                </div>
                                              </div>
                                            </div>
                                                <form action="/weather/remove" method="post">
                                                    <input id="local" name="local" type="hidden" value="{local_id}">
                                                    <input id="remove_id" name="remove_id" type="hidden" value="{r['id']}">
                                                    <input id="remove_forecast" name="remove_forecast" type="hidden" value="{forecast}">
                                                    <button type="submit" class="btn btn-danger btn-sm btn-block" id="{r["id"]}">Remove</button>
                                                </form>
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

    c:edit_comment(\"{comment}\",{location_id},{id})
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
